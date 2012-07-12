from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from mailings.models import DeliveryRecord

class Mailer(object):

    def __init__(self, mailing):
        self.mailing = mailing

    def get_recipients(self):
        return ()

    def build_subject(self, recipient):
        return render_to_string(
            self.mailing.subject_template_name, 
            { 'recipient': recipient, }
        )

    def build_message(self, recipient):
        return render_to_string(
            self.mailing.text_template_name, 
            { 'recipient': recipient, }
        )

    def mail(self):
        recipients = self.get_recipients()
        for r in recipients:
            subject = self.build_subject(r)
            message = self.build_message(r)
            self._send(subject, message, r.email)

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

    def _get_target_models(self):
        return [ct.model_class() for ct in self.mailing.target_types]

class DaysAfterAddedMailer(Mailer):

    def get_recipients(self):
        recipients = []
        # TODO calculate date with self.mailing.days_after_added
        threshold_date = datetime.now() - timedelta(days=self.mailing.days_after_added)
        for m in self._get_target_models():
            recipients += m.objects.filter(added__lte=threshold_date)

        # TODO account for duplicates / allow_duplicates
        return recipients
