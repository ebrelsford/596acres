from email.parser import Parser
from imapclient import IMAPClient

from django.conf import settings

imap = IMAPClient(settings.MAILREADER_HOST, use_uid=True)
imap.login(settings.MAILREADER_HOST_USER, settings.MAILREADER_HOST_PASSWORD)
# TODO MAILREADER_FOLDER? or store on reader model

imap = IMAPClient('mail.webfaction.com', use_uid=True)
imap.login('ebrelsford_596_rcv', 'D1oqsNRJaDKfRNd6QkFb')
imap.select_folder('INBOX')

messages = imap.search(['NOT DELETED'])
response = imap.fetch(messages, ['RFC822'])

parser = Parser()

for uid, message in response:
    parsed = parser.parsestr(message['RFC822'])
    from_address = parsed['From']
    to_address = parsed['To']

    for payload in parsed.get_payload():
        if not payload.is_multipart() and payload.get_content_type() == 'text/plain':
            print payload.get_payload().strip()

    # TODO then mark as deleted?

imap.close_folder()
imap.logout()
