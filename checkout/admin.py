from django.contrib import admin
from .models import Entries

# Register your models here.

class EntriesFilter(admin.ModelAdmin):
    """Filter to make entries model in admin read only"""
    readonly_fields = (
        'user',
        'competition_entry',
        'orderItem',
        'order',
        'ticket_number'
    )

admin.site.register(Entries, EntriesFilter)
