from .mail import mail_lot_organizers, mail_lot_watchers
from .models import Note, Organizer, Picture
from mailutils import mail_facilitators


url_suffixes = {
    Note: '#notes',
    Picture: '#pictures',
    Organizer: '#organizers',
}


def notify_facilitators(obj):
    """
    Send facilitators updates.
    """
    lot = obj.lot
    if not lot: return

    message = _get_object_message(obj)
    kwargs = {
        'borough': lot.borough,
        'is_note': isinstance(obj, Note),
        'lot': lot,
        'obj_url_suffix': url_suffixes[obj.__class__],
    }
    try:
        kwargs['excluded_emails'] = [obj.email]
    except Exception:
        kwargs['excluded_emails'] = []

    mail_facilitators('Lot updated!', message_content=message, **kwargs)


def notify_organizers_and_watchers(obj):
    """
    Send Organizers and Watchers of a given lot updates.
    """
    lot = obj.lot
    if not lot: return

    # don't notify of new organizers when a group already has access
    if lot.group_has_access and isinstance(obj, Organizer): return

    message = _get_object_message(obj)
    kwargs = {}
    try:
        kwargs['excluded_emails'] = [obj.email]
    except Exception:
        kwargs['excluded_emails'] = []
    kwargs['is_note'] = isinstance(obj, Note)
    kwargs['url_suffix'] = url_suffixes[obj.__class__]

    mail_lot_watchers(lot, 'Watched lot updated!', message, **kwargs)
    mail_lot_organizers(lot, 'Organized lot updated!', message, **kwargs)


def _get_object_message(o):
    """
    Get a message specific to the given object.
    """
    # TODO push to templates?
    if isinstance(o, Note):
        return "A note was added by %s:\n\"%s\" " % (o.noter, o.text)
    elif isinstance(o, Picture):
        return 'A new picture was added with the description "%s".' % o.description
    elif isinstance(o, Organizer):
        return "A new organizer named %s was added. " % o.name
    return ""
