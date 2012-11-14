from django.contrib import admin

from actstream.admin import ActionAdmin

from activity_stream.models import PlaceAction

class PlaceActionAdmin(ActionAdmin):
    pass

admin.site.register(PlaceAction, PlaceActionAdmin)
