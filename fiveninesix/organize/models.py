from django.db import models

from lots.models import Lot

class Organizer(models.Model):
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, null=True)
    email = models.EmailField(null=True)
    url = models.URLField(null=True)

    lots = models.ManyToManyField(Lot)
