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

    def place_everything(self, bbox, **kwargs):
        """
        This could work--check all actors, targets, etc, for GeometryFields, 
        get them if they're within the given bbox. Would likely be very 
        inefficient.
        """
        from django.contrib.gis.db.models.fields import GeometryField
        from django.models.db import Q
        from actstream import settings as actstream_settings

        q = Q()
        for model in actstream_settings.get_models().values():
            for field in model._meta._fields():
                if isinstance(field, GeometryField):
                    # TODO add Q() for this field
                    q = q | Q(

                    )
                    pass
