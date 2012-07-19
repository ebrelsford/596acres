from django.core.mail import mail_managers
from django.core.urlresolvers import reverse

from mail import mail_lot_organizers, mail_watchers
from models import Note, Organizer, Picture
from settings import BASE_URL

def new_note_notify_managers(note):
    lot_url = BASE_URL + reverse('lots.views.details', args=(note.lot.bbl,))
    message = """A new note was added on 596acres.org.

Details:
from: %s
text: %s
lot: %s
""" % (note.noter, note.text, lot_url,)

    mail_managers('A new note was created on 596acres.org', message)

def new_organizer_notify_managers(organizer):
    lot_url = BASE_URL + reverse('lots.views.details', args=(organizer.lot.bbl,))
    message = """Neat! A new organizer was created on 596acres.org.

Details:
name: %s
type: %s
phone: %s
email: %s
url: %s
lot: %s
""" % (organizer.name, organizer.type.name, organizer.phone, organizer.email,
       organizer.url, lot_url,)

    mail_managers('A new organizer was created on 596acres.org', message)

def _get_watcher_message(lot, obj_msg, obj_url_suffix=''):
    details_url = BASE_URL + reverse('lots.views.details', kwargs={ 'bbl': lot.bbl }) + obj_url_suffix
    return """Greetings from 596 Acres. There has been a change to a lot you are watching.

%s

View details here: %s """ % (obj_msg, details_url)

def _get_organizer_message(lot, obj_msg, obj_url_suffix=''):
    details_url = (BASE_URL + 
                   reverse('lots.views.details', kwargs={ 'bbl': lot.bbl }) + 
                   obj_url_suffix)
    return """Greetings from 596 Acres. There has been a change to a lot you are organizing.

%s

View details here: %s """ % (obj_msg, details_url)

def _get_object_message(o):
    """
    Get a message specific to the given object.
    """
    if isinstance(o, Note):
        return "A note was added by %s:\n\"%s\" " % (o.noter, o.text)
    elif isinstance(o, Picture):
        return 'A new picture was added with the description "%s".' % o.description
    elif isinstance(o, Organizer):
        return "A new organizer named %s was added. " % o.name
    return ""

def _get_object_url_suffix(o):
    """
    Get a suffix for a url to point to the section of the lot page that will
    contain the given object.
    """
    url_suffix = '#'
    if isinstance(o, Note):
        url_suffix += 'notes'
    elif isinstance(o, Picture):
        url_suffix += 'pictures'
    elif isinstance(o, Organizer):
        url_suffix += 'organizers'
    return url_suffix

def notify_watchers(obj):
    """
    Send watchers of a given lot updates.
    """
    lot = obj.lot
    if not lot:
        return

    obj_msg = _get_object_message(obj)
    url_suffix = _get_object_url_suffix(obj)

    msg = _get_watcher_message(lot, obj_msg, obj_url_suffix=url_suffix)
    mail_watchers(lot, 'Watched lot updated!', msg)

def notify_organizers(obj):
    """
    Send organizers of a given lot updates.
    """
    lot = obj.lot
    if not lot:
        return

    obj_msg = _get_object_message(obj)
    url_suffix = _get_object_url_suffix(obj)

    msg = _get_organizer_message(lot, obj_msg, obj_url_suffix=url_suffix)
    mail_lot_organizers(lot, 'Organized lot updated!', msg, exclude=[obj])
