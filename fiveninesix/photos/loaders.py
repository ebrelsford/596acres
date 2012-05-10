from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal
import json
import os
import urllib2

from django.core.files import File
from models import Photo, PhotoAlbum
from settings import FILE_UPLOAD_TEMP_DIR

# TODO flickr

class PhotoLoader(object):
    def get_updated_photos(self):
        """
        Get a list of Photos that have been updated since the last time they 
        were checked.
        """
        return ()

class FacebookPhotoLoader(PhotoLoader):
    base_url = 'https://graph.facebook.com/'

    def __init__(self, facebook_account):
        super(FacebookPhotoLoader, self).__init__()
        self.facebook_account = facebook_account
        self.last_update_time = facebook_account.last_checked.replace(tzinfo=tzlocal())

    def get_album(self):
        response = urllib2.urlopen(self.base_url + 
                                   self.facebook_account.external_id)
        album = json.loads(response.read())
        return album

    def get_albums(self, url=None):
        if url:
            response = urllib2.urlopen(url)
        else:
            response = urllib2.urlopen(self.base_url + 
                                       self.facebook_account.external_id + '/albums')
        albums = json.loads(response.read())
        try:
            next_page = albums['paging']['next']
        except:
            next_page = None
        return albums['data'], next_page

    def get_photos(self, album, url=None):
        """Get the photos in the given album"""
        if url:
            response = urllib2.urlopen(url)
        else:
            id = self.facebook_account.external_id
            if album:
                id = album['id']
            response = urllib2.urlopen(self.base_url + id + '/photos')
        photos = json.loads(response.read())
        try:
            next_page = photos['paging']['next']
        except:
            next_page = None
        return photos['data'], next_page

    def save_album(self, album):
        """Save the given album, if it's not already saved"""
        local_album, created = PhotoAlbum.objects.get_or_create(
            external_id=album['id'],
            external_source='Facebook',
        )

        # update these fields no matter what
        local_album.name = album.get('name', None)
        local_album.description = album.get('description', None)
        local_album.external_url = album['link']
        local_album.created_time = parse(album['created_time'])
        local_album.updated_time = parse(album['updated_time'])
        local_album.save()
        return local_album

    def save_photo(self, photo, album):
        """Save the given photo, if it's not already saved"""
        # if album doesn't exist, create it
        local_album = self.save_album(album)
        if 'source' not in photo:
            return None

        # if photo doesn't exist, add it to album
        local_photo, created = Photo.objects.get_or_create(
            album=local_album,
            external_id=photo['id'],
            external_source='Facebook',
        )

        # update these fields no matter what
        local_photo.name = photo.get('name', None)
        local_photo.external_url = photo['link']
        local_photo.created_time = parse(photo['created_time'])
        local_photo.updated_time = parse(photo['updated_time'])
        local_photo.position = photo['position']
        local_photo.save()

        # update photo no matter what
        self.download_image(photo['source'], local_photo)

        if local_photo.external_id == album['cover_photo']:
            local_album.cover = local_photo
            local_album.save()
        return local_photo

    def download_image(self, url, local_photo):
        """Download the image at the given url"""
        response = urllib2.urlopen(url)

        # write to temporary file
        temp_file_path = os.sep.join((FILE_UPLOAD_TEMP_DIR, '%s_%s.jpg' % 
                                      (local_photo.external_source,
                                       local_photo.external_id)))
        f = open(temp_file_path, 'wb')
        f.write(response.read())

        # write to field so model will track it
        f = open(temp_file_path, 'rb')
        local_photo.picture.save('%s_%s.jpg' % (local_photo.external_source,
                                                local_photo.external_id), 
                                 File(f))

    def get_updated_photos_for_album(self, album):
        updated_photos = []

        photos, next_page = self.get_photos(album)
        while photos:
            for photo in photos:
                if parse(photo['updated_time']) <= self.last_update_time:
                    continue
                photo = self.save_photo(photo, album)
                if photo:
                    updated_photos.append(photo)
            if not next_page: break
            photos, next_page = self.get_photos(album, url=next_page)
        return updated_photos

    def get_updated_photos_for_albums(self, albums, next_page=None):
        updated_photos = []
        if not albums:
            return []
        for album in albums:
            updated_photos += self.get_updated_photos_for_album(album)
        if next_page:
            albums, next_next_page = self.get_albums(url=next_page)
            return updated_photos + self.get_updated_photos_for_albums(albums, next_page=next_next_page)
        return updated_photos

    def update_last_update_time(self):
        """Update last checked so we don't re-download the photos"""
        self.facebook_account.last_checked = datetime.now()
        self.facebook_account.save()

    def get_updated_photos(self):
        """Get a list of photos that were updated"""
        albums, next_page = self.get_albums()
        if not albums:
            # then hopefully this is an album
            albums = [self.get_album(),]
        updated_photos = self.get_updated_photos_for_albums(albums, next_page=next_page)

        # remember that we've updated the photos for next time
        self.update_last_update_time()
        return updated_photos
