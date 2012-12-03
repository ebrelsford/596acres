from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.geos import Polygon

from actstream.managers import ActionManager, stream

from activity_stream.query import PlaceActivityQuerySet

class PlaceActionManager(GeoManager, ActionManager):
    """
    A Manager that combines GeoManager and ActionManager for a place-based
    Action Manager.
    """
    def get_query_set(self):
        return PlaceActivityQuerySet(self.model, using=self._db)

    @stream
    def in_bbox(self, bbox, **kwargs):
        return self.public(place__within=Polygon.from_bbox(bbox), **kwargs)
