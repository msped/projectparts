from django.contrib import admin
from .models import Product, Categories, Vehicle

# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Vehicle)
