from django.contrib import admin
from django.core.urlresolvers import reverse

from fiveninesix.admin import LotRelatedModelAdmin
from models import Lot, Owner, OwnerType, Review

class LotAdmin(admin.ModelAdmin):
    search_fields = ('address', 'bbl')
    list_display = ('address', 'borough', 'bbl', 'zipcode', 'owner', 'area',)
    list_filter = ('owner__type', 'is_vacant', 'accessible',)
    ordering = ('address',)

class OwnerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'person')
    list_display = ('name', 'code', 'person', 'phone', 'site', 'type',)
    list_filter = ('type',)
    ordering = ('name',)

class OwnerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class ReviewAdmin(LotRelatedModelAdmin):
    search_fields = ('lot__bbl',)
    list_display = ('id', 'in_use', 'accessible', 'should_be_imported', 'imported', 'actual_use', 'reviewer', 'added', 'acres', 'view_lot', 'view_in_oasis', 'change_review',)
    list_editable = ('should_be_imported',)
    list_filter = ('should_be_imported', 'imported', 'in_use', 'accessible', 'needs_further_review', 'added', 'actual_use',)

    def acres(self, obj):
        return obj.lot.area_acres
    acres.admin_order_field = 'lot__area_acres'

    def change_review(self, obj):
        lot = obj.lot
        return '<a target="_blank" href="%s">%s</a>' % (reverse('lots.views.add_review', kwargs={ 'bbl': lot.bbl }), 'change review',)
    change_review.allow_tags = True

admin.site.register(Lot, LotAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerType, OwnerTypeAdmin)
admin.site.register(Review, ReviewAdmin)
