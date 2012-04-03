from apiclient.discovery import build
import httplib2
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from models import Event
from settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

class EventLoader(object):
    def get_updated_events(self):
        """Get a list of Events that have been updated since the last time they were checked"""
        return ()

class GoogleCalendarEventLoader(EventLoader):
    def __init__(self, google_calendar):
        """Get an EventLoader for a GoogleCalendar"""
        super(GoogleCalendarEventLoader, self).__init__()
        self.gcal = google_calendar

    def get_updated_events(self):
        # create and call Google Calendar service
        events_service = self._get_calendar_service().events()
        results = events_service.list(
            calendarId=self.gcal.external_id,
            showDeleted='true',
            singleEvents='true',
            updatedMin=self._get_last_checked()
        ).execute()
        print results

        # save events
        events = results.get('items', ())
        local_events = [self._save_event(e) for e in events]

        # remember that we updated this calendar
        self.gcal.last_checked = datetime.now()
        self.gcal.save()
        return local_events

    def _save_event(self, event):
        """Save the given event"""
        uid = event['id']
        try:
            local_event = Event.objects.get(uid=uid)
        except:
            local_event = Event(uid=uid)

        local_event.calendar = self.gcal
        local_event.author = event['creator']
        local_event.title = event['summary']
        local_event.description = event.get('description', None)
        local_event.location = event.get('location', None)

        local_event.start = parse(event['start']['dateTime'])
        local_event.end = parse(event['end']['dateTime'])

        status = 'active'
        if event['status'] == 'cancelled':
            status = 'cancelled'
        local_event.status = status
        local_event.save()
        return local_event

    def _get_last_checked(self):
        """Get the last time this google calendar was checked, formatted for the request"""
        # add timezone for proper formatting
        return self.gcal.last_checked.replace(tzinfo=tzlocal()).isoformat('T')

    def _get_calendar_service(self):
        """Get the Google Calendar API service for this calendar"""
        FLOW = OAuth2WebServerFlow(
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/calendar',
            user_agent='596acres-calendar-cmdline/1.0')

        storage = Storage(self.gcal.token_file)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
                credentials = run(FLOW, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        return build('calendar', 'v3', http=http)
