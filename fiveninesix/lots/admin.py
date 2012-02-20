from django.contrib import admin
from django.http import HttpResponseRedirect

from models import Lot, Owner, OwnerType, Review

class LotAdmin(admin.ModelAdmin):
    search_fields = ('address', 'bbl')
    list_display = ('address', 'borough', 'bbl', 'zipcode', 'owner', 'area',)
    list_filter = ('owner__type', 'is_vacant',)
    ordering = ('address',)

class OwnerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'person')
    list_display = ('name', 'code', 'person', 'phone', 'site', 'type',)
    list_filter = ('type',)
    ordering = ('name',)

class OwnerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('lot', 'reviewer', 'reviewed', 'acres', 'open_in_oasis',)
    list_filter = ('in_use', 'actual_use', 'accessible', 'needs_further_review',)

    def acres(self, obj):
        return obj.lot.area_acres
    acres.admin_order_field = 'lot__area_acres'

    def open_in_oasis(self, obj):
        return '<a target="_blank" href="http://www.oasisnyc.net/map.aspx?zoomto=lot:%s">OASIS</a>' % (obj.lot.bbl)
    open_in_oasis.allow_tags = True

admin.site.register(Lot, LotAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerType, OwnerTypeAdmin)
admin.site.register(Review, ReviewAdmin)
