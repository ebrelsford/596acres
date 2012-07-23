from hashlib import sha1
import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
import mailchimp
from mailchimp.chimpy.chimpy import ChimpyException

from lots.models import Lot

class Organizer(models.Model):
    """
    Someone organizing around a lot or lots.
    """
    name = models.CharField(_('name'), max_length=256)
    type = models.ForeignKey('OrganizerType')
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
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

    lot = models.ForeignKey(Lot, null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def recent_change_label(self):
        return 'new organizer: %s' % self.name

    class Meta:
        permissions = (
            ('email_organizers', 'Can send an email to all organizers'),
        )

class Watcher(models.Model):
    """
    Someone who is watching a lot.
    """
    name = models.CharField(_('name'), max_length=256)
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    email_hash = models.CharField(max_length=40, null=True, blank=True)
    lot = models.ForeignKey(Lot)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email_hash = sha1(settings.WATCHER_SALT + self.email).hexdigest()
        super(Watcher, self).save(*args, **kwargs)

    def recent_change_label(self):
        return 'new watcher'

    @models.permalink
    def get_edit_url(self):
        return ('organize.views.edit_watcher', (), { 'hash': self.email_hash[:9] })

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

    def __unicode__(self):
        return "%s: %s" % (self.noter, self.text[:50])

    def recent_change_label(self):
        return 'new note: "%s"' % (self.text[:50])

class Picture(models.Model):
    """
    A picture of a lot.
    """
    picture = ImageField(_('picture'), upload_to='pictures')
    description = models.TextField(_('description'), null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot)


#
# Handle signals.
#
from notify import notify_organizers, notify_watchers, new_note_notify_managers

@receiver(post_save, sender=Note, dispatch_uid='note_send_organizer_watcher_update')
@receiver(post_save, sender=Picture, dispatch_uid='picture_send_organizer_watcher_update')
def send_organizer_watcher_update(sender, created=False, instance=None, **kwargs):
    """
    Send organizers and watchers of a given lot updates.
    """
    if instance and created:
        notify_organizers(instance)
        notify_watchers(instance)

        if isinstance(instance, Note):
            new_note_notify_managers(instance)

@receiver(post_save, sender=Organizer, dispatch_uid='organizer_subscribe_organizer_watcher')
@receiver(post_save, sender=Watcher, dispatch_uid='watcher_subscribe_organizer_watcher')
def subscribe_organizer_watcher(sender, created=False, instance=None, **kwargs):
    if not instance or not instance.email:
        return

    if settings.DEBUG:
        logging.debug('Would be subscribing %s to the mailing list' % instance.email)
        return

    try:
        list = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_LIST_ID)
        list.subscribe(instance.email, { 'EMAIL': instance.email, })
    except ChimpyException:
        # thrown if user already subscribed--ignore
        return
