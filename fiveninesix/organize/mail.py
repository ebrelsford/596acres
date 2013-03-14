from django.conf import settings
from django.template.loader import render_to_string

from organize.models import Organizer, Watcher
from mailutils import mail_multiple_personalized, get_message_options


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

    mail_multiple_personalized(
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
    mail_multiple_personalized(subject, messages,
                               **get_message_options(lot, is_note=is_note))


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
    mail_multiple_personalized(subject, messages,
                               **get_message_options(lot, is_note=is_note))


def _get_messages(objs, detail_message, template_name, obj_url_suffix,
                  is_note=False):
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
