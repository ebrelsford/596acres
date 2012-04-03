from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class ExternalCalendar(models.Model):
    """A calendar hosted outside of our site"""
    external_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    last_checked = models.DateTimeField()

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name

class GoogleCalendar(ExternalCalendar):
    """A calendar hosted by google"""
    token_file = models.CharField(max_length=512, help_text='Full path to the OAuth token file')

class Event(models.Model):
    """An event"""
    # from_cal
    calendar_type = models.ForeignKey(ContentType)
    calendar_id = models.PositiveIntegerField()
    calendar = generic.GenericForeignKey('calendar_type', 'calendar_id')

    uid = models.CharField(max_length=256)

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    
    start = models.DateTimeField(help_text='the start time in UTC')
    end = models.DateTimeField(help_text='the end time in UTC')

    STATUS_CHOICES = (
        ('active', 'active',),
        ('cancelled', 'cancelled',),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    
    def __unicode__(self):
        return self.title + str(self.start)   
    
    @models.permalink
    def get_absolute_url(self):
        # TODO implement
        pass
