from mailings.models import Mailing

def send_all(fake=False):
    """
    Send all applicable mailings using the mailer specified by each.
    """
    recipients = []
    for mailing in Mailing.objects.all().select_subclasses():
        recipients.extend(mailing.get_mailer().mail(fake=fake))
    return recipients
