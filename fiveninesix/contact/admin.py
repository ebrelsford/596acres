from django.contrib import admin

from models import JoinUsRequest, LotInformationRequest

class LotInformationRequestAdmin(admin.ModelAdmin):
    search_fields = ('location', 'name',)
    list_display = ('location', 'name', 'email', 'phone', 'handled',)

class JoinUsRequestAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('reason', 'name', 'email', 'phone', 'handled',)

admin.site.register(LotInformationRequest, LotInformationRequestAdmin)
admin.site.register(JoinUsRequest, JoinUsRequestAdmin)
