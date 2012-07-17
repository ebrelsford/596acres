from datetime import datetime, timedelta
from itertools import groupby
import logging

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.db.models import Count
from django.template.loader import render_to_string

from lots.models import Lot
from mailings.models import DeliveryRecord
from organize.models import Watcher

class Mailer(object):

    def __init__(self, mailing):
        self.mailing = mailing
        self.last_checked = self.mailing.last_checked
        self.time_started = datetime.now()

        self.mailing.last_checked = self.time_started
        self.mailing.save()

    def get_recipients(self):
        """
        Get the recipients to which this mailing should be sent.
        """
        return ()

    def get_already_received(self, receiver_type=None):
        """
        Find entities [of a particular type] that already received the mailing.
        """
        drs = DeliveryRecord.objects.filter(
            sent=True, 
            mailing=self.mailing,
        )
        if receiver_type:
            drs = drs.filter(receiver_type=receiver_type)

        # XXX this is not very efficient
        return [r.receiver_object for r in drs]

    def get_context(self, recipients):
        """
        Get the context to be used when constructing the subject and text of 
        the mailing.
        """
        return {
            'mailing': self.mailing,
            'recipients': recipients,
        }

    def build_subject(self, recipients, context):
        return render_to_string(self.mailing.subject_template_name, context)

    def build_message(self, recipients, context):
        return render_to_string(self.mailing.text_template_name, context)

    def add_delivery_records(self, recipients, sent=True):
        """
        Add a DeliveryRecord to each recipient.
        """
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
        Get intended recipients, prepare the message, send it.
        """
        recipients = self.get_recipients()

        # faking it--just add delivery records for recipients and jump out
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
        """
        Build the subject and text of the message, email it to the given 
        email address.
        """
        context = self.get_context(recipients)
        self._send(
            self.build_subject(recipients, context), 
            self.build_message(recipients, context),
            email
        )
        return self.add_delivery_records(recipients)

    def _send(self, subject, message, email_address, 
              from_email=settings.ORGANIZERS_EMAIL, bcc=settings.MANAGERS, 
              connection=None, fail_silently=True):

        logging.debug('mailings: sending mail with subject "%s" to %s' % (subject, email_address))
        logging.debug('mailings: full text: "%s"' % message)

        mail = EmailMultiAlternatives(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            from_email=from_email,
            to=[email_address],
            connection=connection,
            bcc=bcc,
        )          
        mail.send(fail_silently=fail_silently)

class DaysAfterAddedMailer(Mailer):

    def _get_ctype_recipients(self, ctype, delta):
        """
        Get entities of type ctype that should receive the mailing.
        """

        #
        # Check for entities added in the time between the mailing was last 
        # sent and now, shifting backward in time for the number of days after
        # an entity is added that we want to send them the mailing.
        #
        type_recipients = ctype.model_class().objects.filter(
            added__gt=self.last_checked - delta,
            added__lte=self.time_started - delta,
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

        # add BASE_URL for full-path links back to the site
        context['BASE_URL'] = settings.BASE_URL

        # consolidate lots (handy when merging mailings)
        context['lots'] = [r.lot for r in recipients]

        # add url for watchers to edit their watchiness
        if isinstance(recipients[0], Watcher):
            context['edit_url'] = recipients[0].get_edit_url()
        return context

class WatcherThresholdMailer(Mailer):
    def get_recipients(self):
        # get lots without Organizers and with a certain number of Watchers
        lots = Lot.objects.annotate(watcher_count=Count('watcher')).filter(
            organizer=None,
            watcher_count__gte=self.mailing.number_of_watchers
        )

        # get the Watchers of those lots
        watchers = Watcher.objects.filter(lot__in=lots)
        
        received = self.get_already_received()

        return list(set(watchers) - set(received))

    def _get_watcher_count(self, recipients):
        return Lot.objects.filter(id=recipients[0].lot.id).annotate(watcher_count=Count('watcher')).values('watcher_count')[0]['watcher_count']

    def get_context(self, recipients):
        context = super(WatcherThresholdMailer, self).get_context(recipients)

        # add BASE_URL for full-path links back to the site
        context['BASE_URL'] = settings.BASE_URL

        # consolidate lots (handy when merging mailings)
        context['lots'] = [r.lot for r in recipients]

        # add url for watchers to edit their watchiness
        context['edit_url'] = recipients[0].get_edit_url()
        context['watcher_count'] = self._get_watcher_count(recipients)
        return context
