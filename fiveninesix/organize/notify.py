from django.core.mail import mail_managers
from django.core.urlresolvers import reverse

from mail import mail_watchers
from models import Note, Organizer
from settings import BASE_URL

def new_organizer_notify_managers(organizer):
    lots_urls = [BASE_URL + reverse('lots.views.details', args=(l.bbl,)) for l in organizer.lots.all()]
    message = """Neat! A new organizer was created on 596acres.org.

Details:
name: %s
type: %s
phone: %s
email: %s
url: %s
lots: %s
""" % (organizer.name, organizer.type.name, organizer.phone, organizer.email, organizer.url, ', '.join(lots_urls),)

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
    lot = None
    obj_msg = None
    url_suffix = '#'
    if isinstance(obj, Note):
        lot = obj.lot
        obj_msg = "A note was added by %s:\n\"%s\" " % (obj.noter, obj.text)
        url_suffix += 'notes'
    elif isinstance(obj, Organizer):
        lot = obj.lots.all()[0]
        obj_msg = "A new organizer named %s was added. " % obj.name
        url_suffix += 'organizers'

    if lot:
        msg = _get_watcher_message(lot, obj_msg, obj_url_suffix=url_suffix)

        mail_watchers(lot, 'Update!', msg)
