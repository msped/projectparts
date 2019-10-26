from django.contrib import admin
from .models import Competition

# Register your models here.

class competitionAdmin(admin.ModelAdmin):
    exlcude = ('winner',)


admin.site.register(Competition, competitionAdmin)
