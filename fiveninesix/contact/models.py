from django.conf import settings
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from newsletter.util import subscribe

class AbstractContactRequest(models.Model):
    name = models.CharField(_('name'), max_length=128)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=32, null=True, blank=True)

    handled = models.BooleanField(_('handled'), default=False)
    
    class Meta:
        abstract = True

    def get_text_for_mail(self):
        return """name: %s
email: %s
phone: %s
""" % (self.name, self.email, self.phone)

class LotInformationRequest(AbstractContactRequest):
    """A request for more information about a lot, or to give a story about a lot."""
    location = models.TextField(_('location of the lot'))
    story = models.TextField(_('a story about the lot'))
    notes = models.TextField(_('anything else we should know about the lot'),
                             null=True, blank=True)

    def get_text_for_mail(self):
        return super(self.__class__, self).get_text_for_mail() + """location: %s
story: %s
notes: %s
""" % (self.location, self.story, self.notes)

    def get_label_for_mail(self):
        return 'lot information request'

class JoinUsRequest(AbstractContactRequest):
    """A request to help become part of the team."""
    REASON_CHOICES = (
        ('DIST', 'help distribute maps'),
        ('SUGGEST', 'suggest location'),
    )
    reason = models.CharField(_('how I can help'), max_length=16,
                              choices=REASON_CHOICES)
    address = models.CharField(_('where we should put a map?'), max_length=128,
                               null=True, blank=True)

    def get_text_for_mail(self):
        return super(self.__class__, self).get_text_for_mail() + """reason: %s
address: %s
""" % (self.reason, self.address)

    def get_label_for_mail(self):
        return 'map-distribution team submission'

class ContactRequest(AbstractContactRequest):
    """A generic message to the team."""
    message = models.TextField(_('message'))

    def get_text_for_mail(self):
        return super(self.__class__, self).get_text_for_mail() + """message: %s
""" % (self.message,)

    def get_label_for_mail(self):
        return 'message'


@receiver(post_save, dispatch_uid='contact_model_saved')
def contact_model_saved(sender, created=False, instance=None, **kwargs):
    if created and issubclass(sender, AbstractContactRequest):
        _send_email_for_request(instance)
        subscribe(instance)

def _send_email_for_request(request):
    admin_url = settings.BASE_URL + reverse('admin:%s_%s_change' % (request._meta.app_label, request.__class__.__name__.lower()), args=(request.id,))
    mail_managers(
        'A new %s was sent via 596acres.org' % request.get_label_for_mail(), 
        """Oh man! A new %s was sent via 596acres.org.
        
Details: 
%s

View on the site: %s

Thanks! Have a lovely day.
""" % (request.get_label_for_mail(), request.get_text_for_mail(), admin_url))
