from django.contrib import admin

from mailings.models import DaysAfterAddedMailing, DeliveryRecord,\
        SuccessfulOrganizerMailing, WatcherThresholdMailing

class DaysAfterAddedMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked', 'days_after_added',)

class SuccessfulOrganizerMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked',)

class WatcherThresholdMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked', 'number_of_watchers',)

class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = ('receiver_object', 'mailing', 'sent', 'recorded',)

admin.site.register(DaysAfterAddedMailing, DaysAfterAddedMailingAdmin)
admin.site.register(DeliveryRecord, DeliveryRecordAdmin)
admin.site.register(SuccessfulOrganizerMailing, SuccessfulOrganizerMailingAdmin)
admin.site.register(WatcherThresholdMailing, WatcherThresholdMailingAdmin)
