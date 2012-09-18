from email import message_from_string
from imapclient import IMAPClient

from django.conf import settings

def get_mail():
    imap = IMAPClient(settings.MAILREADER_HOST, use_uid=True)
    imap.login(settings.MAILREADER_HOST_USER, settings.MAILREADER_HOST_PASSWORD)
    imap.select_folder('INBOX')

    messages = imap.search(['NOT SEEN'])
    response = imap.fetch(messages, ['RFC822'])

    mail = []

    for uid, message in response.items():
        parsed = message_from_string(message['RFC822'])
        payloads = []
        for payload in parsed.get_payload():
            if not payload.is_multipart() and payload.get_content_type() == 'text/plain':
                payloads.append(payload.get_payload().strip())
        mail.append({
            'from_address': parsed['From'],
            'payloads': payloads,
            'subject': parsed['Subject'],
            'to_address': parsed['To'],
        })

    imap.close_folder()
    imap.logout()

    return mail
