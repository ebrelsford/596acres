from django.contrib import admin

from mailings.models import DaysAfterAddedMailing, DeliveryRecord

class DaysAfterAddedMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_after_added', 'target_types',)

class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = ('receiver_object', 'mailing', 'sent', 'recorded',)

admin.site.register(DaysAfterAddedMailing, DaysAfterAddedMailingAdmin)
admin.site.register(DeliveryRecord, DeliveryRecordAdmin)
