from django.contrib import admin

from models import Note, Organizer, OrganizerType, Watcher, Picture

class OrganizerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'email', 'phone', 'url',)

class OrganizerTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_group',)

class WatcherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name', 'email', 'phone',)

class NoteAdmin(admin.ModelAdmin):
    search_fields = ('noter', 'text')
    list_display = ('noter', 'text')

class PictureAdmin(admin.ModelAdmin):
    list_display = ('picture', 'added')

admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Note, NoteAdmin)

