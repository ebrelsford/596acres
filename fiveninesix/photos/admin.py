from django.contrib import admin

from models import FacebookPhotoAccount, FacebookPhotoAlbum, Photo, PhotoAlbum

class FacebookPhotoAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'last_checked',)

class FacebookPhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'last_checked',)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'album',)

class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id',)

admin.site.register(FacebookPhotoAccount, FacebookPhotoAccountAdmin)
admin.site.register(FacebookPhotoAlbum, FacebookPhotoAlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
