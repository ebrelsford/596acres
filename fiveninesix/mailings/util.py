import sys
import traceback

from mailings.models import Mailing

def send_all(fake=False):
    """
    Send all applicable mailings using the mailer specified by each.
    """
    recipients = []
    for mailing in Mailing.objects.all().select_subclasses():
        try:
            recipients.extend(mailing.get_mailer().mail(fake=fake))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            print "There was an exception while sending mailing", mailing
            continue
    return recipients
