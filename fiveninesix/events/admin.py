from django.contrib import admin

from models import Event, GoogleCalendar

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'status', 'location',) # TODO in local time

class GoogleCalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked',)   

admin.site.register(Event, EventAdmin)
admin.site.register(GoogleCalendar, GoogleCalendarAdmin)
