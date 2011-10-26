from django.core.mail.message import EmailMultiAlternatives

from models import Organizer, Watcher
import settings

def mail_organizers(subject, message, fail_silently=False, connection=None, html_message=None):             
    """Sends a message to all organizers."""
    organizers = Organizer.objects.filter(email__isnull=False)
    _mail_multiple(subject, message, [o.email for o in organizers], fail_silently=fail_silently, connection=connection, html_message=html_message)

def mail_watchers(lot, subject, message, fail_silently=False, connection=None, html_message=None):             
    """Sends a message to watchers of a given lot."""
    watchers = Watcher.objects.filter(lot=lot, email__isnull=False)
    _mail_multiple(subject, message, [w.email for w in watchers], fail_silently=fail_silently, connection=connection, html_message=html_message)

def _mail_multiple(subject, message, email_addresses, fail_silently=False, connection=None, html_message=None):
    """Sends a message to multiple email addresses. Based on django.core.mail.mail_admins()"""
    mail = EmailMultiAlternatives(u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message, from_email=settings.SERVER_EMAIL,
                                  to=email_addresses, connection=connection, bcc=settings.MANAGERS)          
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)

