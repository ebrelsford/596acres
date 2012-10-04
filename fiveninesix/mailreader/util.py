from collections import Iterable
from email import message_from_string
from imapclient import IMAPClient

from django.conf import settings

def login():
    """
    Log in to the mailbox we will read from.
    """
    imap = IMAPClient(settings.MAILREADER_HOST, use_uid=True)
    imap.login(settings.MAILREADER_HOST_USER, settings.MAILREADER_HOST_PASSWORD)
    imap.select_folder('INBOX')
    return imap

def get_messages(imap):
    """
    Get messages from the given server.
    """
    messages = imap.search(['NOT SEEN'])
    return imap.fetch(messages, ['RFC822'])

def consolidate_payloads(payload):
    """
    Get text from a message's payload.
    """
    if isinstance(payload, str):
        return (payload,)
    elif isinstance(payload, Iterable):
        return filter(None, [consolidate_payloads(p) for p in payload])
    elif not payload.is_multipart() and payload.get_content_type() == 'text/plain':
        return payload.get_payload().strip()

def get_mail():
    imap = login()
    response = get_messages(imap)

    mail = []
    for uid, message in response.items():
        parsed = message_from_string(message['RFC822'])
        mail.append({
            'from_address': parsed['From'],
            'payloads': consolidate_payloads(parsed.get_payload()),
            'subject': parsed['Subject'],
            'to_address': parsed['To'],
        })

    imap.close_folder()
    imap.logout()

    return mail
