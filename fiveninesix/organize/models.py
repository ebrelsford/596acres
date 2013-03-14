from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField

from lots.models import Lot
from newsletter.util import subscribe


class Participant(models.Model):
    name = models.CharField(_('name'), max_length=256)
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'))
    email_hash = models.CharField(max_length=40, null=True, blank=True)
    lot = models.ForeignKey(Lot)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email_hash = sha1(settings.PARTICIPANT_SALT + self.email).hexdigest()
        super(Participant, self).save(*args, **kwargs)

    @models.permalink
    def get_edit_url(self):
        return ('organize.views.edit_participant', (), { 'hash': self.email_hash[:9] })


class Organizer(Participant):
    """
    Someone organizing around a lot or lots.
    """
    # so we can do spatial joins between Organizer and Lot
    objects = models.GeoManager()

    type = models.ForeignKey('OrganizerType')
    url = models.URLField(_('url'), null=True, blank=True)
    notes = models.TextField(_('notes'), null=True, blank=True)
    facebook_page = models.CharField(
        _('facebook page'),
        max_length=256,
        null=True,
        blank=True,
        help_text=('The Facebook page for your organization. Please do not '
                   'enter your personal Facebook page.'),
    )

    def recent_change_label(self):
        return 'new organizer: %s' % self.name

    class Meta:
        permissions = (
            ('email_organizers', 'Can send an email to all organizers'),
        )

    def get_absolute_url(self):
        return "%s#organizer-%d" % (self.lot.get_absolute_url(), self.pk)


class Watcher(Participant):
    """
    Someone who is watching a lot.
    """
    # so we can do spatial joins between Watcher and Lot
    objects = models.GeoManager()

    def recent_change_label(self):
        return 'new watcher'


class OrganizerType(models.Model):
    """
    A type of organizer (eg, individual, non-profit, governmental agency, ...)
    """
    name = models.CharField(max_length=64)
    is_group = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Meeting(models.Model):
    """
    A meeting organized regarding a lot or lots.
    """
    name = models.CharField(max_length=256)
    description = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=256)

    organizer = models.ForeignKey(Organizer)
    lots = models.ManyToManyField(Lot, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Note(models.Model):
    """
    A note about a lot.
    """
    noter = models.CharField(_('your name'), max_length=256)
    text = models.TextField(_('note'))
    added = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot)
    added_by = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.noter, self.text[:50])

    def recent_change_label(self):
        return 'new note: "%s"' % (self.text[:50])

    def get_absolute_url(self):
        return "%s#note-%d" % (self.lot.get_absolute_url(), self.pk)


class Picture(models.Model):
    """
    A picture of a lot.
    """
    picture = ImageField(_('picture'), upload_to='pictures')
    description = models.TextField(_('description'), null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot)
    added_by = models.ForeignKey(User, null=True, blank=True)


#
# Handle signals.
#
from activity_stream.signals import action
from notify import notify_organizers_and_watchers, notify_facilitators


def _get_verb(sender):
    default = 'added'
    if isinstance(sender, Note):
        return 'wrote'
    if isinstance(sender, Organizer):
        return 'started organizing'
    if isinstance(sender, Picture):
        # TODO link to picture
        return 'posted a picture'
    if isinstance(sender, Watcher):
        return 'started watching'
    return default


def _get_actor(instance, added_by):
    default = added_by

    # Hold on to Organizer instance as actor
    if isinstance(instance, Organizer):
        return instance

    # Don't keep track of the user who created the Watcher--keep anonymous
    if isinstance(instance, Watcher):
        return None

    return default


@receiver(post_save, sender=Note, dispatch_uid='organize.models.add_action')
@receiver(post_save, sender=Organizer, dispatch_uid='organize.models.add_action')
@receiver(post_save, sender=Picture, dispatch_uid='organize.models.add_action')
@receiver(post_save, sender=Watcher, dispatch_uid='organize.models.add_action')
def add_action(sender, created=False, instance=None, **kwargs):
    if not instance or not created:
        return
    action.send(
        _get_actor(instance, instance.added_by),
        verb=_get_verb(instance),
        action_object=instance, # action object, what was created
        place=instance.lot.centroid, # where did it happen?
        target=instance.lot, # what did it happen to?
        data={},
    )


@receiver(post_save, sender=Note, dispatch_uid='note_send_organizer_watcher_update')
@receiver(post_save, sender=Picture, dispatch_uid='picture_send_organizer_watcher_update')
def send_organizer_watcher_update(sender, created=False, instance=None, **kwargs):
    """
    Send organizers and watchers of a given lot updates.
    """
    if instance and created:
        notify_organizers_and_watchers(instance)
        notify_facilitators(instance)


@receiver(post_save, sender=Organizer, dispatch_uid='organizer_subscribe_organizer_watcher')
@receiver(post_save, sender=Watcher, dispatch_uid='watcher_subscribe_organizer_watcher')
def subscribe_organizer_watcher(sender, created=False, instance=None, **kwargs):
    if created:
        subscribe(instance, is_participating=True)
