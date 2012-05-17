from django.contrib import admin
from django.core.urlresolvers import reverse

from fiveninesix.admin import LotRelatedModelAdmin, view_in_oasis
from models import Lot, Owner, OwnerType, Review, ExtendedDetails

class ExtendedDetailsInline(admin.StackedInline):
    model = ExtendedDetails

class LotAdmin(admin.ModelAdmin):
    search_fields = ('address', 'bbl')
    list_display = (
        'address', 'borough', 'bbl', 'zipcode', 'owner', 'area',
        'jurisdiction_code', 'jurisdiction_description', 'agency_codes',
        'current_uses', 'primary_use', 'rpad_description',
        'is_vacant',
        'view_in_oasis',
    )
    list_filter = ('owner__type', 'is_vacant', 'accessible', 'borough', 'extendeddetails__current_uses',)
    ordering = ('borough', 'bbl',)
    fieldsets = (
        (None, {
            'fields': (
                'bbl', 
                ('address', 'borough', 'zipcode',),
                ('area', 'area_acres',),
                'owner',
                ('is_vacant', 'actual_use', 'accessible',),
                'group_has_access',
            ),
        }),
        ('Advanced Details', {
            'classes': ('collapse',),
            'fields': (
                ('block', 'lot',),
                ('school_district', 'fire_comp', 'health_area', 'health_ctr'),
                'police_precinct',
                ('assess_land', 'assess_total', 'exempt_land', 'exempt_total',),
                'centroid',
                'centroid_source',
                'polygon',
                'qrcode',
            ),
        }),
    )
    inlines = (ExtendedDetailsInline,)

    def jurisdiction_description(self, obj):
        return obj.extendeddetails.jurisdiction_description
    jurisdiction_description.admin_order_field = 'extendeddetails__jurisdiction_description'

    def jurisdiction_code(self, obj):
        return obj.extendeddetails.jurisdiction_code
    jurisdiction_code.admin_order_field = 'extendeddetails__jurisdiction_code'

    def agency_codes(self, obj):
        return obj.extendeddetails.agency_codes
    agency_codes.admin_order_field = 'extendeddetails__agency_codes'

    def rpad_description(self, obj):
        return obj.extendeddetails.rpad_description
    rpad_description.admin_order_field = 'extendeddetails__rpad_description'

    def primary_use(self, obj):
        return obj.extendeddetails.primary_use
    primary_use.admin_order_field = 'extendeddetails__primary_use'

    def current_uses(self, obj):
        return obj.extendeddetails.current_uses
    current_uses.admin_order_field = 'extendeddetails__current_uses'

    def view_in_oasis(self, obj):
        return view_in_oasis(obj)
    view_in_oasis.allow_tags = True

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
