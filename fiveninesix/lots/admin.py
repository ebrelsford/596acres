from django.contrib import admin

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
    list_display = ('lot', 'reviewer', 'reviewed')

admin.site.register(Lot, LotAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerType, OwnerTypeAdmin)
admin.site.register(Review, ReviewAdmin)
