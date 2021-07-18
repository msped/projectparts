from django.contrib import admin
from .models import Product, Categories, Vehicle, Manufacturer, Fitments

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name', 'ticket_price', 'product_price')}

admin.site.register(Categories)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vehicle)
admin.site.register(Manufacturer)
admin.site.register(Fitments)
