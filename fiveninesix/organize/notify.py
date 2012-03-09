from django.core.mail import mail_managers
from django.core.urlresolvers import reverse

from mail import mail_watchers
from models import Note, Organizer
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
""" % (organizer.name, organizer.type.name, organizer.phone, organizer.email, organizer.url, lot_url,)

    mail_managers('A new organizer was created on 596acres.org', message)

def _get_watcher_message(lot, obj_msg, obj_url_suffix=''):
    details_url = BASE_URL + reverse('lots.views.details', kwargs={ 'bbl': lot.bbl }) + obj_url_suffix
    return """Greetings from 596 Acres. There has been a change to a lot you are watching.

%s

View details here: %s """ % (obj_msg, details_url)

def notify_watchers(obj):
    """
    Send watchers of a given lot updates.
    """
    lot = obj.lot
    obj_msg = None
    url_suffix = '#'
    if isinstance(obj, Note):
        obj_msg = "A note was added by %s:\n\"%s\" " % (obj.noter, obj.text)
        url_suffix += 'notes'
    elif isinstance(obj, Organizer):
        obj_msg = "A new organizer named %s was added. " % obj.name
        url_suffix += 'organizers'

    if lot:
        msg = _get_watcher_message(lot, obj_msg, obj_url_suffix=url_suffix)

        mail_watchers(lot, 'Watched lot updated!', msg)
