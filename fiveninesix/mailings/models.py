from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Mailing(models.Model):
    """
    An email that should be sent to an entity.
    """
    name = models.CharField(max_length=100)

    allow_duplicates = models.BooleanField(
        default=False,
        help_text=('This mailing should be sent to the same email address '
                   'multiple times.'),
    )

    subject_template_name = models.CharField(max_length=256)
    text_template_name = models.CharField(max_length=256)

    target_types = models.ManyToManyField(ContentType)

    def __unicode__(self):
        return self.name

class DaysAfterAddedMailing(Mailing):
    """
    An email that should be sent to an entity X days after being added.
    """
    days_after_added = models.IntegerField(
        help_text=('The number of days after an entity is added that they '
                   'should receive an email.'),
    )

class DeliveryRecord(models.Model):
    """
    The record of a mailing being sent.
    """
    sent = models.BooleanField(
        default=False,
        help_text='The mailing was sent.',                      
    )

    recorded = models.DateTimeField(
        auto_now_add=True,
        help_text='When this mailing was recorded.',
    )

    mailing = models.ForeignKey(
        Mailing,
        help_text='The mailing that was sent.',
    )

    receiver_type = models.ForeignKey(ContentType, null=True, blank=True)
    receiver_object_id = models.PositiveIntegerField(null=True, blank=True)
    receiver_object = generic.GenericForeignKey('receiver_type', 'receiver_object_id')
