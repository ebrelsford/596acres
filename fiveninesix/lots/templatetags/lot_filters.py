from django import template
from django.utils.safestring import mark_safe

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
    return mark_safe(lot.display_name)


@register.filter
def lot_contact(lot):
    """
    Get the contact information for the given lot.
    """
    if lot.owner.type.name == 'city':
        if lot.owner_contact:
            return '%s (%s)' % (lot.owner_contact.name, lot.owner_contact.phone)
        else:
            return '%s (%s)' % (lot.owner.person, lot.owner.phone)
    elif lot.owner.type.name == 'private':
        return '596acres@gmail.com to learn more'
