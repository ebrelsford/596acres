"""
Utilities for sending mail.
"""
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


def mail_facilitators(subject, message_content=None,
                      message_template='organize/notifications/facilitators_text.txt',
                      borough=None, excluded_emails=[],
                      lot=None, is_note=False, **kwargs):
    """
    Sends a message to facilitators.
    """
    facilitators = []
    facilitators += settings.FACILITATORS['global']
    facilitators += settings.FACILITATORS.get(borough, [])
    facilitators = [f for f in facilitators if f not in excluded_emails]

    messages = _get_facilitator_messages(
        facilitators,
        message_template,
        is_note=is_note,
        lot=lot,
        message=message_content,
        **kwargs
    )
    mail_multiple_personalized(subject, messages, fail_silently=False,
                               **get_message_options(lot, is_note=is_note))


def _get_facilitator_messages(facilitators, template_name, **kwargs):
    messages = {}
    context = kwargs
    context.update({
        'BASE_URL': settings.BASE_URL,
        'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
    })
    for facilitator in facilitators:
        messages[facilitator] = render_to_string(template_name, context)
    return messages


def mail_multiple_personalized(subject, messages, **kwargs):
    for email, message in messages.items():
        mail_multiple(subject, message, [email], **kwargs)


def mail_multiple(subject, message, email_addresses,
                   from_email=settings.ORGANIZERS_EMAIL, cc=None, bcc=None,
                   html_message=None, connection=None, fail_silently=True):
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


def get_message_options(lot, is_note=False):
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
