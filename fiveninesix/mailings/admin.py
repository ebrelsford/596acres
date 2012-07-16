from django.contrib import admin

from mailings.models import DaysAfterAddedMailing, DeliveryRecord, WatcherThresholdMailing

class DaysAfterAddedMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_after_added',)

class WatcherThresholdMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_watchers',)

class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = ('receiver_object', 'mailing', 'sent', 'recorded',)

admin.site.register(DaysAfterAddedMailing, DaysAfterAddedMailingAdmin)
admin.site.register(DeliveryRecord, DeliveryRecordAdmin)
admin.site.register(WatcherThresholdMailing, WatcherThresholdMailingAdmin)
