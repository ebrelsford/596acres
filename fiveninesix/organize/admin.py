from django.contrib import admin

from models import Organizer, OrganizerType, Watcher

class OrganizerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'email', 'phone', 'url',)

class OrganizerTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_group',)

class WatcherAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name', 'email', 'phone',)

admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)
admin.site.register(Watcher, WatcherAdmin)

