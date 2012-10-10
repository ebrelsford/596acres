from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string

from organize.models import Organizer, Watcher

def mail_organizers(subject, message, public_no_access=False, 
                    public_access=False, private_access=False, **kwargs):
    """
    Sends a message to organizers. Can filter by the type of land and the 
    status of the organizing.
    """
    organizers = Organizer.objects.filter(email__isnull=False).exclude(email='')

    if not all((public_no_access, public_access, private_access)):
        f = Q()

        if public_no_access:
            f = f | Q(lot__group_has_access=False, lot__owner__type__name='city')
        if public_access:
            f = f | Q(lot__group_has_access=True, lot__owner__type__name='city')
        if private_access:
            f = f | Q(lot__group_has_access=True, lot__owner__type__name='private')

        organizers = organizers.filter(f)

    messages = {}
    for organizer in organizers:
        messages[organizer.email] = render_to_string(
            'organize/notifications/mass_organizer_text.txt', 
            {
                'BASE_URL': settings.BASE_URL,
                'lot': organizer.lot,
                'message': message,
                'organizer': organizer,
            }
        )

    _mail_multiple_personalized(
        subject, 
        messages, 
        from_email=settings.ORGANIZERS_EMAIL, 
        **kwargs
    )

def mail_lot_organizers(lot, subject, message, exclude=[], is_note=False, url_suffix=''):
    """
    Sends a message to organizers of a given lot or group of lots.
    """
    organizers = Organizer.objects.filter(lot__in=lot.lots, email__isnull=False)
    organizers = [o for o in organizers if o not in exclude]
    messages = _get_messages(
        organizers,
        message,
        'organize/notifications/organizers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages, **_get_message_options(lot, is_note=is_note))

def mail_watchers(lot, subject, message, is_note=False, url_suffix=''):
    """
    Sends a message to watchers of a given lot or group of lots.
    """
    watchers = Watcher.objects.filter(lot__in=lot.lots, email__isnull=False)
    messages = _get_messages(
        watchers,
        message,
        'organize/notifications/watchers_text.txt',
        url_suffix,
        is_note=is_note,
    )
    _mail_multiple_personalized(subject, messages, **_get_message_options(lot, is_note=is_note))

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
        'cc': [settings.ORGANIZERS_EMAIL],
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
