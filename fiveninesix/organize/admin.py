from django.contrib import admin

from fiveninesix.admin import LotRelatedModelAdmin
from models import Note, Organizer, OrganizerType, Watcher, Picture

class OrganizerAdmin(LotRelatedModelAdmin):
    search_fields = ('name', 'email',)
    list_display = ('name', 'email', 'phone', 'url', 'lot_owner', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)

    def lot_owner(self, obj):
        return obj.lot.owner
    lot_owner.admin_order_field = 'lot__owner__name'

class OrganizerTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_group',)

class WatcherAdmin(LotRelatedModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name', 'email', 'phone', 'lot', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)

class NoteAdmin(LotRelatedModelAdmin):
    search_fields = ('noter', 'text')
    list_display = ('noter', 'text', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)

class PictureAdmin(LotRelatedModelAdmin):
    list_display = ('picture', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)

admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Note, NoteAdmin)
