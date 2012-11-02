from django.contrib.gis.measure import Distance

from lots.models import Lot

def get_nearby(lot, count=5, distance=Distance(mi=.25)):
    nearby_lots = Lot.objects.filter(
        centroid__distance_lte=(lot.centroid, distance),
        lotlayer__name__in=(
            'organizing_sites',
            'private_accessed_sites',
            'public_accessed_sites',
            'vacant_sites',
        ),
    ).exclude(pk=lot.pk).distance(lot.centroid).order_by('distance')
    if nearby_lots.count() > count:
        nearby_lots = nearby_lots[:count]
    return nearby_lots
