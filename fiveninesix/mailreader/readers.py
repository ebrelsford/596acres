import re

from django.conf import settings

from lots.models import Lot
from organize.models import Note

class MailReader(object):
    from_name_regex = '(.+?)\s.+'
    from_name_pattern = re.compile(from_name_regex)

    def get_name(self, address):
        """
        Try to get an acceptable name from an email address.
        """
        try:
            name = self.from_name_pattern.match(address).group(1)
        except Exception:
            name = address.split('@')[0]
        return name

    def should_read(self, from_address=None, to_address=None, subject=None,
                    payloads=None, **kwargs):
        """
        Should this reader read this mail?
        """
        return False

    def read(self, from_address=None, to_address=None, subject=None,
             payloads=None, **kwargs):
        """
        Attempt to read the given mail. Return True if successful, False 
        otherwise.
        """
        return False

class NotesMailReader(MailReader): 
    bbl_regex = '(?:.*\s+)?<?notes\+(\d+)@.+>?'
    bbl_pattern = re.compile(bbl_regex)

    cutoff_line_pattern = '.*%s.*' % settings.MAILREADER_REPLY_PREFIX

    gmail_prefix = re.compile('.*On .+ wrote:.*')

    # These line patterns gathered using emails received and some tips as 
    # suggested here:
    #  http://stackoverflow.com/questions/278788/parse-email-content-from-quoted-reply
    #  http://stackoverflow.com/questions/824205/while-processing-an-email-reply-how-can-i-ignore-any-email-client-specifics-th
    reply_prefixes = (
        gmail_prefix, # gmail, yahoo
        re.compile('^Date:.*'), # hotmail
        re.compile('^.*---+.*'), # outlook express
        re.compile('^.*___+.*'), # outlook
        re.compile('^Sent from my .+'), # common mobile signature
    )

    def should_read(self, from_address=None, to_address=None, subject=None,
                    payloads=None, **kwargs):
        if from_address in settings.MAILREADER_IGNORE_FROM: return False
        return 'notes' in to_address

    def get_lot(self, to_address):
        """
        Get the lot using the address the message was sent to, which should
        include a BBL.
        """
        try:
            bbl = self.bbl_pattern.match(to_address).group(1)
            return Lot.objects.get(bbl=bbl)
        except Exception:
            return None

    def remove_lines_after(self, lines, pattern):
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                return lines[:i]
        return lines

    def get_note_text(self, from_address, payload_text):
        """
        Try to get the text that the sender sent. Since the email will likely
        be in response to another email, we have to try to get rid of the
        original message and any extra text the sender's email client put 
        between the sender's message and the original.
        """
        lines = payload_text.split('\r\n')
        try:
            # Use our cutoff line, which is added to messages that will be
            # replied to, to get rid of most of the quoted text.
            lines = self.remove_lines_after(lines, self.cutoff_line_pattern)

            # chop off empty lines at the end
            while lines[-1] == '':
                lines = lines[:-1]

            # Now chop off common signatures and lines prefixed to replied-to
            # messages.
            if '@gmail.com' in from_address:
                # gmail wraps these lines often
                gmail_test = ''.join(lines[-2:])
                if re.match(self.gmail_prefix, gmail_test):
                    lines = lines[:-2]
            for prefix in self.reply_prefixes:
                lines = self.remove_lines_after(lines, prefix)

        except Exception:
            pass
        return '\n'.join(lines).strip()

    def read(self, from_address=None, to_address=None, subject=None, 
             payloads=None, verbose=False, **kwargs):
        lot = self.get_lot(to_address)
        if not lot:
            return False

        combined_payloads = '\r\n'.join(payloads)

        if verbose:
            print 'Starting with:'
            print '=============='
            print combined_payloads

        text = self.get_note_text(from_address, combined_payloads)

        if verbose:
            print 'Ended up with:'
            print '=============='
            print text

        note = Note(
            lot=lot,
            noter=self.get_name(from_address),
            text=text,
        )
        note.save()
        return True
