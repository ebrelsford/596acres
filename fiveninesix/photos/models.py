from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField

class ExternalPhotoSet(models.Model):
    """A set of photos hosted outside of our site"""
    external_id = models.CharField(_('external id'), max_length=256)
    name = models.CharField(_('name'), max_length=256)
    last_checked = models.DateTimeField(_('last checked'))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class FacebookPhotoAccount(ExternalPhotoSet):
    """An account for which all photos should be mirrored"""

    def __unicode__(self):
        return self.name

class FacebookPhotoAlbum(ExternalPhotoSet):
    """An album for which all photos should be mirrored"""

    def __unicode__(self):
        return self.name

class PhotoAlbum(models.Model):
    name = models.CharField(_('name'), max_length=256, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    external_source = models.CharField(max_length=32, blank=True, null=True)
    external_id = models.CharField(max_length=256, blank=True, null=True)
    external_url = models.CharField(max_length=512, blank=True, null=True)

    cover = models.ForeignKey('Photo', blank=True, null=True)

    created_time = models.DateTimeField(_('created time'), blank=True, 
                                        null=True)
    updated_time = models.DateTimeField(_('updated time'), blank=True, 
                                        null=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    parent_album = models.ForeignKey('self', related_name='children',
                                     blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('photos_photoalbum_detail', (), {
            'pk': self.pk,
        })

    def _get_photos(self):
        """
        Get photos that are in this album or in child albums of this album.
        """
        photos = list(self.photo_set.all())
        for child in self.children.all():
            photos += child.photos
        return photos
    photos = property(_get_photos)

    def get_cover_photo(self):
        """
        Get the photo that should be the cover for this album.
        """
        if self.cover: return self.cover
        return self.photos[0]

class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True)
    name = models.TextField(_('name'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    external_source = models.CharField(max_length=32, blank=True, null=True)
    external_id = models.CharField(max_length=256, blank=True, null=True)
    external_url = models.CharField(max_length=512, blank=True, null=True)

    picture = ImageField(_('picture'), upload_to='mirrored_pictures')
    created_time = models.DateTimeField(_('created time'), blank=True, 
                                        null=True)
    updated_time = models.DateTimeField(_('updated time'), blank=True, 
                                        null=True)
    position = models.PositiveIntegerField(_('position'), blank=True, 
                                           null=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return 'photo: ' + (self.name or 'unnamed')

    @models.permalink
    def get_absolute_url(self):
        return ('photos_photo_detail', (), {
            'album_id': self.album.pk,
            'pk': self.pk,
        })
