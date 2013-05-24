from django.contrib.gis.measure import Distance
from django.utils.translation import ugettext_lazy as _

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


def _lot_name_chunk_text(names, label, plural_label=None):
    """
    Consolidate a chunk of a lot group's name (borough, block, or lot).
    """
    if len(names) == 1:
        return names[0], label
    else:
        return ', '.join(sorted(names)), plural_label or label + 's'


def get_lot_group_name(lots):
    """
    Get a display name for this lot group.
    """
    borough_names = []
    block_names = []
    lot_names = []

    for l in lots:
        borough_names.append(l.borough)
        block_names.append(l.block)
        lot_names.append(l.lot)

    borough_names = list(set(borough_names))
    block_names = list(set(block_names))
    lot_names = list(set(lot_names))

    borough_text, borough_label = _lot_name_chunk_text(borough_names, 'borough')
    block_text, block_label = _lot_name_chunk_text(block_names, 'block')
    lot_text, lot_label = _lot_name_chunk_text(lot_names, 'lot')

    return "%s %s %s, %s %s" % (
        borough_text,
        _(block_label),
        block_text,
        _(lot_label),
        lot_text,
    )
