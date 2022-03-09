from django.contrib import admin
from .models import Competition

# Register your models here.

class CompetitionAdmin(admin.ModelAdmin):
    """Custom admin so that the winner cant be changed on the dashboard to
    keep the competition fair"""
    readonly_fields = ('winner',)


admin.site.register(Competition, CompetitionAdmin)
