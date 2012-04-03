from django.core.management.base import BaseCommand, CommandError

from events.loaders import GoogleCalendarEventLoader
from events.models import GoogleCalendar

class Command(BaseCommand):
    help = 'Update all calendars, adding events to the database as necessary'

    def handle(self, *args, **options):
        """Update all calendars"""
        try:
            for gcal in GoogleCalendar.objects.all():
                self.stdout.write('Updating events for Google Calendar "%s"...' % gcal.name)
                events = GoogleCalendarEventLoader(gcal).get_updated_events()
                self.stdout.write('added or updated %d events.\n' % len(events))
        except:
            raise CommandError('There was an exception while updating calendars')
