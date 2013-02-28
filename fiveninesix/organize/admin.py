from django.contrib import admin

from fiveninesix.admin import LotRelatedModelAdmin
from models import Note, Organizer, OrganizerType, Watcher, Picture

class OrganizerAdmin(LotRelatedModelAdmin):
    list_display = ('name', 'email', 'phone', 'added', 'lot_owner', 'view_lot',
                    'view_in_oasis',)
    list_filter = ('added', 'lot__borough',)
    readonly_fields = ('lot',)
    search_fields = ('name', 'email', 'lot__bbl',)

    def lot_owner(self, obj):
        return obj.lot.owner
    lot_owner.admin_order_field = 'lot__owner__name'

class OrganizerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group',)
    search_fields = ('name',)

class WatcherAdmin(LotRelatedModelAdmin):
    list_display = ('name', 'email', 'phone', 'lot', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)
    search_fields = ('name', 'email', 'lot__bbl',)

class NoteAdmin(LotRelatedModelAdmin):
    list_display = ('noter', 'text', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)
    search_fields = ('noter', 'text', 'lot__bbl',)

class PictureAdmin(LotRelatedModelAdmin):
    list_display = ('picture', 'added', 'view_lot', 'view_in_oasis',)
    list_filter = ('added',)

admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Note, NoteAdmin)
