from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def lot_ownercount(lot, arg=None):
    return len(set([l.owner for l in lot.lots]))

@register.filter
def lot_acres_sum(lot):
    return mark_safe(sum([l.area_acres for l in lot.lots]))

@register.filter
def lot_tab_label(lot):
    if len(lot.group) <= 3:
        return lot.bbl
    elif len(lot.group) <= 5:
        return 'lot %s' % lot.lot
    else:
        return lot.lot

@register.filter
def lot_short_description(lot):
    if lot.group_has_access:
        return mark_safe('-- a group has access here')
    if 'organizing_sites' in lot.lotlayer_set.all().values_list('name', flat=True):
        return mark_safe('-- a group is organizing here')
    return ''

@register.filter
def lotname(lot, arg=None):
    """
    Get a display name for the given lot or lot group.
    """
    if lot.children.count > 1 and arg == 'group':
        return mark_safe(_lot_group_name(lot.lots))
    else:
        return mark_safe(_lot_individual_name(lot))

def _lot_individual_name(lot):
    """
    Get a display name for this lot.
    """
    return "%s %s %s, %s %s" % (
        lot.borough,
        _('block'),
        lot.block,
        _('lot'),
        lot.lot,
    )

def _lot_name_chunk_text(names, label, plural_label=None):
    """
    Consolidate a chunk of a lot group's name (borough, block, or lot).
    """
    if len(names) == 1:
        return names[0], label
    else:
        return ', '.join(sorted(names)), plural_label or label + 's'

def _lot_group_name(lots):
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
