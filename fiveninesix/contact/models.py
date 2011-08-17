from django.core.mail import mail_managers
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from settings import BASE_URL

class AbstractContactRequest(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32, null=True, blank=True)

    handled = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def get_text_for_mail(self):
        return """name: %s
email: %s
phone: %s
""" % (self.name, self.email, self.phone)

class LotInformationRequest(AbstractContactRequest):
    """A request for more information about a lot, or to give a story about a lot."""
    location = models.TextField('location of the lot')
    story = models.TextField('a story about the lot')
    notes = models.TextField('anything else we should know about the lot', null=True, blank=True)

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
    reason = models.CharField("how I can help", max_length=16, choices=REASON_CHOICES)
    address = models.CharField('where we should put a map?', max_length=128, null=True, blank=True)

    def get_text_for_mail(self):
        return super(self.__class__, self).get_text_for_mail() + """reason: %s
address: %s
""" % (self.reason, self.address)

    def get_label_for_mail(self):
        return 'map-distribution team submission'

class ContactRequest(AbstractContactRequest):
    """A generic message to the team."""
    message = models.TextField()

    def get_text_for_mail(self):
        return super(self.__class__, self).get_text_for_mail() + """message: %s
""" % (self.message,)

    def get_label_for_mail(self):
        return 'message'

@receiver(post_save, sender=ContactRequest, dispatch_uid='contact_model_saved')
def contact_model_saved(sender, **kwargs):
    if issubclass(sender, AbstractContactRequest):
        _send_email_for_request(kwargs['instance'])

def _send_email_for_request(request):
    admin_url = BASE_URL + reverse('admin:%s_%s_change' % (request._meta.app_label, request.__class__.__name__.lower()), args=(request.id,))
    mail_managers(
        'A new %s was sent via 596acres.org' % request.get_label_for_mail(), 
        """Oh man! A new %s was sent via 596acres.org.
        
Details: 
%s

View on the site: %s

Thanks! Have a lovely day.
""" % (request.get_label_for_mail(), request.get_text_for_mail(), admin_url))
