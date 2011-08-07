from django.db import models

class LotInformationRequest(models.Model):
    location = models.TextField('location of the lot')
    story = models.TextField('a story about the lot')
    notes = models.TextField('anything else we should know about the lot', null=True, blank=True)

    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32, null=True, blank=True)

    handled = models.BooleanField(default=False)

class JoinUsRequest(models.Model):
    REASON_CHOICES = (
        ('DIST', 'help distribute maps'),
        ('SUGGEST', 'suggest location'),
    )
    reason = models.CharField("how I can help", max_length=16, choices=REASON_CHOICES)
    address = models.CharField('where we should put a map?', max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32, null=True, blank=True)

    handled = models.BooleanField(default=False)

class ContactRequest(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32, null=True, blank=True)
    message = models.TextField()

    handled = models.BooleanField(default=False)
