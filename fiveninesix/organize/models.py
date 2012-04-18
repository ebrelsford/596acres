from hashlib import sha1

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import ImageField

from lots.models import Lot
from settings import WATCHER_SALT

class Organizer(models.Model):
    """
    Someone organizing around a lot or lots.
    """
    name = models.CharField(max_length=256)
    type = models.ForeignKey('OrganizerType')
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    facebook_page = models.CharField(max_length=256, null=True, blank=True)

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
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_hash = models.CharField(max_length=40, null=True, blank=True)
    lot = models.ForeignKey(Lot)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email:
            self.email_hash = sha1(WATCHER_SALT + self.email).hexdigest()
        super(Watcher, self).save(*args, **kwargs)

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
    noter = models.CharField(max_length=256, verbose_name='your name')
    text = models.TextField(verbose_name='note')
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
    picture = ImageField(upload_to='pictures')
    description = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot)


#
# Handle signals.
#
from notify import notify_watchers, new_note_notify_managers

@receiver(post_save, sender=Note)
@receiver(post_save, sender=Picture)
def send_watcher_update(sender, created=False, instance=None, **kwargs):
    """
    Send watchers of a given lot updates.
    """
    if instance and created:
        notify_watchers(instance)

        if isinstance(instance, Note):
            new_note_notify_managers(instance)
