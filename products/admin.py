from django.contrib import admin
from .models import Product, Categories, Vehicle, Manufacturer, Fitments

# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(Manufacturer)
admin.site.register(Fitments)
