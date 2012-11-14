from django.contrib.gis.db.models.query import GeoQuerySet

from actstream.gfk import GFKQuerySet

class PlaceActivityQuerySet(GeoQuerySet, GFKQuerySet):
    """
    A QuerySet that combines GeoQuerySet and GFKQuerySet.
    """
    pass
