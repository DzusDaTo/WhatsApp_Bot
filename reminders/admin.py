from django.contrib import admin
from .models import Reminder


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'message', 'send_time', 'created_at', 'updated_at')
    list_filter = ('send_time',)
    search_fields = ('phone_number', 'message')
    ordering = ('send_time',)


admin.site.register(Reminder, ReminderAdmin)
