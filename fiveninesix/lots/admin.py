from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.core.urlresolvers import reverse

from fiveninesix.admin import LotRelatedModelAdmin, view_in_oasis
from models import Lot, Owner, OwnerContact, OwnerType, Review, ExtendedDetails

class ExtendedDetailsInline(admin.StackedInline):
    model = ExtendedDetails

class LotAdmin(OSMGeoAdmin):
    default_lon = -8234558.58109
    default_lat = 4963211.58171
    default_zoom = 10

    search_fields = ('address', 'bbl')
    list_display = (
        'address', 'borough', 'bbl', 'zipcode', 'owner', 'area',
        'is_vacant',
        'view_in_oasis',
    )
    list_filter = ('owner__type', 'is_vacant', 'accessible', 'borough', 'extendeddetails__current_uses',)
    ordering = ('borough', 'bbl',)
    fieldsets = (
        (None, {
            'fields': (
                ('bbl', 'name',),
                ('address', 'borough', 'zipcode',),
                ('area', 'area_acres',),
                ('owner', 'owner_contact',),
                ('is_vacant', 'actual_use', 'accessible',),
                ('group_has_access', 'group_with_access',),
            ),
        }),
        ('Advanced Details', {
            'classes': ('collapse',),
            'fields': (
                'parent_lot',
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

    def current_uses(self, obj):
        return obj.extendeddetails.current_uses
    current_uses.admin_order_field = 'extendeddetails__current_uses'

    def view_in_oasis(self, obj):
        return view_in_oasis(obj)
    view_in_oasis.allow_tags = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent_lot':
            kwargs['queryset'] = Lot.objects.all().order_by('bbl')
            return db_field.formfield(**kwargs)
        return super(LotAdmin, self).formfield_for_foreignkey(db_field,
                                                              request, **kwargs)

class OwnerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'person')
    list_display = ('name', 'code', 'person', 'phone', 'site', 'type',)
    list_filter = ('type',)
    ordering = ('name',)

class OwnerContactAdmin(admin.ModelAdmin):
    search_fields = ('name', 'owner')
    list_display = ('name', 'owner', 'jurisdiction', 'notes', 'phone', 'email',)
    list_filter = ('owner',)
    ordering = ('owner', 'name',)

class OwnerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class ReviewAdmin(LotRelatedModelAdmin):
    search_fields = ('lot__bbl',)
    list_display = ('id', 'in_use', 'accessible', 'should_be_imported', 'imported', 'actual_use', 'reviewer', 'added', 'acres', 'view_lot', 'view_in_oasis', 'change_review',)
    list_editable = ('should_be_imported',)
    list_filter = ('lot__borough', 'should_be_imported', 'imported', 'in_use',
                   'accessible', 'needs_further_review', 'added', 'actual_use',)

    def acres(self, obj):
        return obj.lot.area_acres
    acres.admin_order_field = 'lot__area_acres'

    def change_review(self, obj):
        lot = obj.lot
        return '<a target="_blank" href="%s">%s</a>' % (reverse('lots.views.add_review', kwargs={ 'bbl': lot.bbl }), 'change review',)
    change_review.allow_tags = True

admin.site.register(Lot, LotAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
admin.site.register(OwnerType, OwnerTypeAdmin)
admin.site.register(Review, ReviewAdmin)
