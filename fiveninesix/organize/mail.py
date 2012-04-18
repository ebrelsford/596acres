from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse

from organize.models import Organizer, Watcher
import settings

def mail_organizers(subject, message, fail_silently=False, connection=None, html_message=None):             
    """Sends a message to all organizers."""
    organizers = Organizer.objects.filter(email__isnull=False).exclude(email='')
    _mail_multiple(subject, message, [o.email for o in organizers], fail_silently=fail_silently, connection=connection, html_message=html_message, from_email=settings.ORGANIZERS_EMAIL)

def mail_watchers(lot, subject, message, fail_silently=False, connection=None, html_message=None):             
    """Sends a message to watchers of a given lot."""
    watchers = Watcher.objects.filter(lot=lot, email__isnull=False)
    messages = {}
    for watcher in watchers:
        edit_url = settings.BASE_URL + reverse('organize.views.edit_watcher', kwargs={ 'hash': watcher.email_hash[:9], })
        messages[watcher.email] = message + """

You are receiving this email because you are watching lot %s on 596acres.org. Please go here if you would like to change this: %s
""" % (lot.bbl, edit_url)
        pass
    _mail_multiple_personalized(subject, messages, fail_silently=fail_silently, connection=connection, html_message=html_message)

def _mail_multiple_personalized(subject, messages, fail_silently=False, connection=None, html_message=None):
    for email, message in messages.items():
        _mail_multiple(subject, message, [email], fail_silently=fail_silently, connection=connection, html_message=html_message)

def _mail_multiple(subject, message, email_addresses, fail_silently=False, connection=None, html_message=None, from_email=settings.SERVER_EMAIL):
    """Sends a message to multiple email addresses. Based on django.core.mail.mail_admins()"""
    for email_address in email_addresses:
        mail = EmailMultiAlternatives(u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message, from_email=from_email,
                                      to=[email_address], connection=connection, bcc=settings.MANAGERS)          
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
