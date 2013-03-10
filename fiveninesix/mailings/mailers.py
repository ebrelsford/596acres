from datetime import datetime, timedelta
from itertools import groupby
import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail.message import EmailMessage
from django.db.models import Count
from django.template.loader import render_to_string

from lots.models import Lot
from mailings.models import DeliveryRecord
from organize.models import Organizer, Watcher


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
        return [r.receiver_object for r in drs if r.receiver_object is not None]

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
              from_email=settings.ORGANIZERS_EMAIL,
              bcc=[settings.ORGANIZERS_EMAIL], connection=None,
              fail_silently=True):

        subject = subject.replace('\n', '').strip() # subject cannot contain newlines

        logging.debug('mailings: sending mail with subject "%s" to %s' % (subject, email_address))
        logging.debug('mailings: full text: "%s"' % message)

        mail = EmailMessage(
            u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message,
            from_email=from_email,
            to=[email_address],
            connection=connection,
            bcc=bcc,
        )
        mail.send(fail_silently=fail_silently)


class DaysAfterAddedMailer(Mailer):

    def get_recipient_queryset(self, model):
        """
        Check for entities added in the time between the last time the mailing
        was sent and now, shifting backward in time for the number of days
        after an entity is added that we want to send them the mailing.
        """
        delta = timedelta(days=self.mailing.days_after_added)
        return model.objects.filter(
            added__gt=self.last_checked - delta,
            added__lte=self.time_started - delta,
            email__isnull=False,
        ).exclude(email='')

    def _get_ctype_recipients(self, ctype):
        """
        Get entities of type ctype that should receive the mailing.
        """
        type_recipients = self.get_recipient_queryset(ctype.model_class())

        # only get already received if there are potential recipients
        if not type_recipients:
            return []

        received = self.get_already_received(receiver_type=ctype)

        return list(set(type_recipients) - set(received))

    def get_recipients(self):
        recipient_lists = [self._get_ctype_recipients(ct) for ct in self.mailing.target_types.all()]
        return reduce(lambda x,y: x+y, recipient_lists)

    def get_context(self, recipients):
        context = super(DaysAfterAddedMailer, self).get_context(recipients)
        context['has_received_this_mailing'] = self.has_received(
            self.mailing,
            recipients[0]
        )
        return context

    def has_received(self, mailing, recipient):
        other_pks = recipient.__class__.objects.filter(
            email=recipient.email
        ).exclude(pk=recipient.pk).values_list('pk', flat=True)

        records = DeliveryRecord.objects.filter(
            mailing=mailing,
            receiver_object_id__in=other_pks,
            receiver_type=ContentType.objects.get_for_model(recipient)
        )
        return records.count() > 0


class SuccessfulOrganizerMailer(Mailer):
    def get_recipient_queryset(self, ctype, already_received):
        # successful organizers / watchers
        qs = ctype.model_class().objects.filter(lot__group_has_access=True)

        # remove lots where anyone else on this lot has received this mailing.
        # these people are latecomers and congratulating them would be a bit
        # weird.
        #
        # NB: if a person is the first of a type (eg, Watcher) and the lot
        # already had access, they will get this message anyway. this will be
        # such a rare case that we will let it happen.
        lots_already_recevieved = list(set([r.lot for r in already_received]))
        qs = qs.exclude(lot__in=lots_already_recevieved)

        return qs

    def _get_ctype_recipients(self, ctype):
        """
        Get entities of type ctype that should receive the mailing.
        """
        received = self.get_already_received(receiver_type=ctype)
        type_recipients = self.get_recipient_queryset(ctype, received)

        return list(set(type_recipients) - set(received))

    def get_context(self, recipients):
        context = super(SuccessfulOrganizerMailer, self).get_context(recipients)

        # add BASE_URL for full-path links back to the site
        context['BASE_URL'] = settings.BASE_URL

        context['lot'] = recipients[0].lot
        return context

    def get_recipients(self):
        recipient_lists = [self._get_ctype_recipients(ct) for ct in self.mailing.target_types.all()]
        return reduce(lambda x,y: x+y, recipient_lists)


class DaysAfterWatcherOrganizerAddedMailer(DaysAfterAddedMailer):
    """
    DaysAfterAddedMailer customized for 596.
    """
    def get_recipient_queryset(self, model):
        qs = super(DaysAfterWatcherOrganizerAddedMailer, self).get_recipient_queryset(model)
        if model == Organizer:
            # don't email welcome / two-week followup to Organizers of lots
            #  that have been accessed
            qs = qs.filter(
                lot__group_has_access=False,

                # sandy
                lot__sandy_distribution_site=False,
                lot__sandy_dropoff_site=False,
            )
        return qs

    def get_context(self, recipients):
        context = super(DaysAfterWatcherOrganizerAddedMailer, self).get_context(recipients)

        # add BASE_URL for full-path links back to the site
        context['BASE_URL'] = settings.BASE_URL

        # consolidate lots (handy when merging mailings)
        context['lots'] = [r.lot for r in recipients]

        # url for changing what one's organizing/watching
        context['edit_url'] = recipients[0].get_edit_url()
        return context


class WatcherThresholdMailer(Mailer):
    def get_recipients(self):
        # get lots without Organizers and with a certain number of Watchers
        lots = Lot.objects.annotate(watcher_count=Count('watcher')).filter(
            organizer=None,
            watcher_count__gte=self.mailing.number_of_watchers,

            # sandy
            sandy_distribution_site=False,
            sandy_dropoff_site=False,
        )

        # get the Watchers of those lots
        watchers = Watcher.objects.filter(lot__in=lots)

        received = self.get_already_received()

        return list(set(watchers) - set(received))

    def _get_watcher_count(self, recipients):
        lots = Lot.objects.filter(id=recipients[0].lot.id)
        lots = lots.annotate(watcher_count=Count('watcher'))
        return lots.values('watcher_count')[0]['watcher_count']

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
