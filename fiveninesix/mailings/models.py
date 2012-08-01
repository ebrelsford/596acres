from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

class Mailing(models.Model):
    """
    An email that should be sent to an entity. The email can be sent 
    automatically by polling over the entities that should receive it.

    Subclass Mailing and specify a Mailer to create a mailing. Use mixins 
    rather than deep inheritance hierarchies since polymorphic methods only
    work on direct descendants of this using InheritanceManager.
    """
    objects = InheritanceManager()

    name = models.CharField(_('name'), max_length=100)

    HANDLING_CHOICES = (
        ('each', 'send each'),
        ('first', 'send first'),
        ('merge', 'merge'),
    )
    duplicate_handling = models.CharField(
        _('duplicate handling'),
        max_length=32,
        choices=HANDLING_CHOICES,
        default='each',
        help_text=('How should we handle mailings that are going to go to the '
                   'same email address multiple times?'),
    )

    subject_template_name = models.CharField(
        _('subject template name'),
        max_length=256,
        help_text=('The path to the template to use when building the mailing '
                   'subject line'),
    )
    text_template_name = models.CharField(
        _('text template name'),
        max_length=256,
        help_text=('The path to the template to use when building the mailing '
                   'text line'),
    )

    target_types = models.ManyToManyField(
        ContentType,
        help_text='The types this mailing will be sent to.',
        verbose_name=_('target types'),
    )

    last_checked = models.DateTimeField(
        _('last checked'),
        help_text='The last time this mailing was sent.'
    )

    def __unicode__(self):
        return self.name

    def get_mailer(self):
        raise Exception('Subclasses of Mailing must define get_mailer()')

class DaysAfterAddedMixin(models.Model):
    """
    An email that should be sent to an entity a certain number of days after 
    the entity is added.

    Entities should have two fields:
        'email'
        'added'
    """
    days_after_added = models.IntegerField(
        _('days after added'),
        help_text=('The number of days after an entity is added that they '
                   'should receive an email.'),
    )

    class Meta:
        abstract = True

class DeliveryRecord(models.Model):
    """
    The record of a mailing being sent.
    """
    sent = models.BooleanField(
        _('sent'),
        default=False,
        help_text='The mailing was sent.',                      
    )

    recorded = models.DateTimeField(
        _('recorded'),
        auto_now_add=True,
        help_text='When this mailing was recorded.',
    )

    mailing = models.ForeignKey(
        Mailing,
        help_text='The mailing that was sent.',
    )

    receiver_type = models.ForeignKey(ContentType, null=True, blank=True)
    receiver_object_id = models.PositiveIntegerField(null=True, blank=True)
    receiver_object = generic.GenericForeignKey('receiver_type', 'receiver_object_id')

from mailings.mailers import DaysAfterWatcherOrganizerAddedMailer,\
        SuccessfulOrganizerMailer, WatcherThresholdMailer

class DaysAfterAddedMailing(Mailing, DaysAfterAddedMixin):
    def get_mailer(self):
        return DaysAfterWatcherOrganizerAddedMailer(self)

class SuccessfulOrganizerMailing(Mailing):
    def get_mailer(self):
        return SuccessfulOrganizerMailer(self)

class WatcherThresholdMailing(Mailing):
    number_of_watchers = models.PositiveIntegerField(
        help_text=('The number of watchers on a lot required before the '
                   'mailing is sent to all of them.'),
    )

    def get_mailer(self):
        return WatcherThresholdMailer(self)
