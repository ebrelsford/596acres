from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from mailutils import mail_facilitators
from newsletter.util import subscribe


class AbstractContactRequest(models.Model):
    name = models.CharField(_('name'), max_length=128)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)

    BOROUGH_CHOICES = (
        ('Brooklyn', 'Brooklyn'),
        ('Bronx', 'Bronx'),
        ('Manhattan', 'Manhattan'),
        ('Queens', 'Queens'),
        ('Staten Island', 'Staten Island'),
    )
    borough = models.CharField(_('borough'), max_length=32, null=True,
                               blank=True, choices=BOROUGH_CHOICES)

    handled = models.BooleanField(_('handled'), default=False)

    class Meta:
        abstract = True


class LotInformationRequest(AbstractContactRequest):
    """
    A request for more information about a lot, or to give a story about a lot.
    """
    location = models.TextField(_('location of the lot'))
    story = models.TextField(_('a story about the lot'))
    notes = models.TextField(_('anything else we should know about the lot'),
                             null=True, blank=True)

    def get_label_for_mail(self):
        return 'lot information request'


class ContactRequest(AbstractContactRequest):
    """A generic message to the team."""

    REASON_CHOICES = (
        ('visioning', _('request a community land access workshop')),
        ('lot_in_life', _('tell us about the lot in your life')),
        ('event', _('invite us to your event')),
        ('press', _('press inquiry')),
        ('other_city', _("I'm in a city that's not New York")),
        ('other', _('other')),
    )
    reason = models.CharField(_('reason'), max_length=32,
                              choices=REASON_CHOICES, default='other',
                              help_text=_('Why are you contacting us?'))

    message = models.TextField(_('message'))

    def get_label_for_mail(self):
        return 'message'


@receiver(post_save, dispatch_uid='contact_model_saved')
def contact_model_saved(sender, created=False, instance=None, **kwargs):
    if created and issubclass(sender, AbstractContactRequest):
        _send_email_for_contact_request(instance)
        subscribe(instance)


def _send_email_for_contact_request(contact_request):
    recipients = None
    if contact_request.reason in ('other', 'other_city', 'press',):
        recipients = settings.CONTACT_TARGETS.get(contact_request.reason)
    elif contact_request.reason is 'event' and contact_request.borough is None:
        recipients = settings.CONTACT_TARGETS.get(contact_request.reason)

    mail_facilitators(
        ('A new %s was sent via 596acres.org'
            % contact_request.get_label_for_mail()),
        message_template='contact/notifications/facilitators_text.txt',
        borough=contact_request.borough,
        contact_request=contact_request,
        recipients=recipients,
    )
