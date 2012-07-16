from datetime import datetime, timedelta
from itertools import groupby

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from mailings.models import DeliveryRecord, DaysAfterWatcherOrganizerAddedMailing
from organize.models import Watcher

_registry = {}

def register_mailer(mailing_class, mailer_class):
    _registry[mailing_class.__name__] = mailer_class

def get_mailer_class(mailing):
    return _registry[mailing.__class__.__name__]

class Mailer(object):

    def __init__(self, mailing):
        self.mailing = mailing
        self.last_checked = self.mailing.last_checked
        self.time_started = datetime.now()

        self.mailing.last_checked = self.time_started
        self.mailing.save()

    def get_recipients(self):
        return ()

    def get_context(self, recipients):
        return {
            'mailing': self.mailing,
            'recipients': recipients,
        }

    def build_subject(self, recipients):
        return render_to_string(
            self.mailing.subject_template_name, 
            self.get_context(recipients)
        )

    def build_message(self, recipients):
        return render_to_string(
            self.mailing.text_template_name, 
            self.get_context(recipients)
        )

    def add_delivery_records(self, recipients, sent=True):
        drs = []
        for recipient in recipients:
            dr = DeliveryRecord(
                sent=sent,
                mailing=self.mailing,
                receiver_object=recipient
            )
            dr.save()
            drs.append(dr)
        return drs

    def mail(self, fake=False):
        """
        Get intended recipients, prepare message, send it.
        """
        recipients = self.get_recipients()

        # just add delivery records for recipients and jump out
        if fake:
            self.add_delivery_records(recipients)
            return recipients

        duplicate_handling = self.mailing.duplicate_handling
        if duplicate_handling in ('merge', 'send first'):
            # group by email address to handle duplicates
            for email, recipient_group in groupby(recipients, lambda r: r.email):
                if duplicate_handling == 'send first':
                    recipient_group = [recipient_group[0]]
                self._prepare_and_send_message(list(recipient_group), email)
        else:
            # don't bother grouping--every recipient gets every message
            for r in recipients:
                self._prepare_and_send_message([r], r.email)
        return recipients

    def _prepare_and_send_message(self, recipients, email):
        subject = self.build_subject(recipients)
        message = self.build_message(recipients)
        self._send(subject, message, email)
        return self.add_delivery_records(recipients)

    def _send(self, subject, message, email_address, 
              from_email=settings.SERVER_EMAIL, bcc=settings.MANAGERS, 
              connection=None, fail_silently=True):

        mail = EmailMultiAlternatives(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            from_email=from_email,
            to=[email_address],
            connection=connection,
            bcc=bcc,
        )          
        mail.send(fail_silently=fail_silently)

    def get_already_received(self, receiver_type=None):
        """Find entities that already received the mailing"""
        drs = DeliveryRecord.objects.filter(
            sent=True, 
            mailing=self.mailing,
        )
        if receiver_type:
            drs = drs.filter(receiver_type=receiver_type)
        return [r.receiver_object for r in drs]

class DaysAfterAddedMailer(Mailer):

    def _get_ctype_recipients(self, ctype, delta):
        # get entities that should receive the mailing
        type_recipients = ctype.model_class().objects.filter(
            added__lte=self.time_started - delta,
            added__gt=self.last_checked - delta,
            email__isnull=False,
        ).exclude(email='')

        received = self.get_already_received(receiver_type=ctype)

        return list(set(type_recipients) - set(received))

    def get_recipients(self):
        delta = timedelta(days=self.mailing.days_after_added)

        recipient_lists = [self._get_ctype_recipients(ct, delta) for ct in self.mailing.target_types.all()]
        return reduce(lambda x,y: x+y, recipient_lists)

class DaysAfterWatcherOrganizerAddedMailer(DaysAfterAddedMailer):
    """
    DaysAfterAddedMailer customized for 596.
    """
    def get_context(self, recipients):
        context = super(DaysAfterWatcherOrganizerAddedMailer, self).get_context(recipients)
        context['BASE_URL'] = settings.BASE_URL
        context['lots'] = [r.lot for r in recipients]

        if recipients[0].__class__ == Watcher:
            context['edit_url'] = recipients[0].get_edit_url()
        return context

class WatcherThresholdMailer(Mailer):
    # TODO implement
    pass

def send_all(fake=False):
    recipients = []
    for mailing in DaysAfterWatcherOrganizerAddedMailing.objects.all():
        mailer_class = get_mailer_class(mailing)
        recipients.extend(mailer_class(mailing).mail(fake=fake))
    return recipients
