from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from organize.models import Organizer, Watcher

def mass_mailing(subject, message, objects, template_name, **kwargs):
    messages = {}
    for obj in objects:
        # message gets sent once to each unique email address, thanks to dict
        messages[obj.email] = render_to_string(template_name, {
            'BASE_URL': settings.BASE_URL,
            'lot': obj.lot,
            'message': message,
            'obj': obj,
        })

    _mail_multiple_personalized(
        subject, 
        messages, 
        from_email=settings.ORGANIZERS_EMAIL,
        **kwargs
    )

def mass_mail_watchers(subject, message, watchers, **kwargs):
    """
    Sends a message to watchers.
    """
    mass_mailing(
        subject,
        message,
        watchers,
        'organize/notifications/mass_watcher_text.txt',
        **kwargs
    )

def mass_mail_organizers(subject, message, organizers, **kwargs):
    """
    Sends a message to organizers.
    """
    mass_mailing(
        subject,
        message,
        organizers,
        'organize/notifications/mass_organizer_text.txt',
        **kwargs
    )

def mail_lot_organizers(lot, subject, message, excluded_emails=[],
                        is_note=False, url_suffix=''):
    """
    Sends a message to organizers of a given lot or group of lots.
    """
    organizers = Organizer.objects.filter(lot__in=lot.lots, email__isnull=False)
    organizers = [o for o in organizers if o.email not in excluded_emails]
    messages = _get_messages(
        organizers,
        message,
        'organize/notifications/organizers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages,
                                **_get_message_options(lot, is_note=is_note))

def mail_lot_watchers(lot, subject, message, excluded_emails=[], is_note=False,
                      url_suffix=''):
    """
    Sends a message to watchers of a given lot or group of lots.
    """
    watchers = Watcher.objects.filter(lot__in=lot.lots, email__isnull=False)
    watchers = [w for w in watchers if w.email not in excluded_emails]
    messages = _get_messages(
        watchers,
        message,
        'organize/notifications/watchers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages,
                                **_get_message_options(lot, is_note=is_note))

def _get_messages(objs, detail_message, template_name, obj_url_suffix, is_note=False):
    messages = {}
    for o in objs:
        messages[o.email] = render_to_string(template_name, {
            'BASE_URL': settings.BASE_URL,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
            'is_note': is_note,
            'lot': o.lot,
            'message': detail_message,
            'obj': o,
            'obj_url_suffix': obj_url_suffix,
        })
    return messages

def _get_message_options(lot, is_note=False):
    if not is_note: return {}
    return {
        'from_email': _get_lot_email_address(lot),
        'cc': None,
        'bcc': None,
    }

def _get_lot_email_address(lot):
    """
    Get the from email for the given lot.
    """
    return '"596 Acres Lot %s" <notes+%s@596acres.org>' % (lot.bbl, lot.bbl,)

def _mail_multiple_personalized(subject, messages, **kwargs):
    for email, message in messages.items():
        _mail_multiple(subject, message, [email], **kwargs)

def _mail_multiple(subject, message, email_addresses, 
                   from_email=settings.ORGANIZERS_EMAIL, cc=None,
                   bcc=settings.MANAGERS, html_message=None, connection=None,
                   fail_silently=True):
    """
    Sends a message to multiple email addresses. Based on 
    django.core.mail.mail_admins()
    """
    for email_address in email_addresses:
        mail = EmailMultiAlternatives(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            bcc=bcc,
            cc=cc,
            connection=connection,
            from_email=from_email,
            to=[email_address],
        )          
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
