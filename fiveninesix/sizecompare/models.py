from django.db import models
from django.utils.translation import ugettext_lazy as _

class SizeComparable(models.Model):
    name = models.CharField(_('name'), max_length=256)
    sqft = models.IntegerField(_('square feet'))

    # TODO location, description, url, ...

    def __unicode__(self):
        return self.name
