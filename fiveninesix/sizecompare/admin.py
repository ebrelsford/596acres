from django.contrib import admin

from sizecompare.models import SizeComparable

class SizeComparableAdmin(admin.ModelAdmin):
    list_display = ('name', 'sqft',)
    search_fields = ('name',)

admin.site.register(SizeComparable, SizeComparableAdmin)
