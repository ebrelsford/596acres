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
    message = models.TextField(_('message'))

    def get_label_for_mail(self):
        return 'message'


@receiver(post_save, dispatch_uid='contact_model_saved')
def contact_model_saved(sender, created=False, instance=None, **kwargs):
    if created and issubclass(sender, AbstractContactRequest):
        _send_email_for_contact_request(instance)
        subscribe(instance)


def _send_email_for_contact_request(contact_request):
    mail_facilitators(
        'A new %s was sent via 596acres.org' % contact_request.get_label_for_mail(),
        message_template='contact/notifications/facilitators_text.txt',
        borough=contact_request.borough,
        contact_request=contact_request,
    )
