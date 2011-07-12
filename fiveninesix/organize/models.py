from django.db import models

from lots.models import Lot

class Organizer(models.Model):
    """
    Someone organizing around a lot or lots.
    """
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    lots = models.ManyToManyField(Lot)
    type = models.ForeignKey('OrganizerType')

    def __unicode__(self):
        return self.name

class OrganizerType(models.Model):
    """
    A type of organizer (eg, individual, non-profit, governmental agency, ...)
    """
    name = models.CharField(max_length=64)
    is_group = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Meeting(models.Model):
    """
    A meeting organized regarding a lot or lots.
    """
    name = models.CharField(max_length=256)
    description = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=256)

    organizer = models.ForeignKey(Organizer)
    lots = models.ManyToManyField(Lot, null=True, blank=True)

    def __unicode__(self):
        return self.name
