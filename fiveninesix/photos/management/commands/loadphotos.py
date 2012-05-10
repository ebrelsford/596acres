import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from photos.loaders import FacebookPhotoLoader
from photos.models import FacebookPhotoAlbum, FacebookPhotoAccount

class Command(BaseCommand):
    help = 'Update all photos, adding to the database as necessary'

    def handle(self, *args, **options):
        """Update all photos"""
        try:
            for album in FacebookPhotoAlbum.objects.all():
                self.stdout.write('Updating photos for Facebook Photo Album "%s"...' % album.name)
                events = FacebookPhotoLoader(album).get_updated_photos()
                self.stdout.write('added or updated %d photos.\n' % len(events))

            for account in FacebookPhotoAccount.objects.all():
                self.stdout.write('Updating photos for Facebook Account "%s"...' % account.name)
                events = FacebookPhotoLoader(account).get_updated_photos()
                self.stdout.write('added or updated %d photos.\n' % len(events))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('There was an exception while updating photos')
