from django.contrib import admin
from .models import Product, Categories, Vehicle, Manufacturer

# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(Manufacturer)
