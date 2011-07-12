from django.contrib import admin

from models import Organizer, OrganizerType, Meeting

class OrganizerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'email', 'phone', 'url',)

class OrganizerTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_group',)

admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)

