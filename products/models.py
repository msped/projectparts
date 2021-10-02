from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Vehicle(models.Model):
    """Model for Make and model of vehicles"""
    make = models.CharField(default='', max_length=50)
    model = models.CharField(default='', max_length=100)
    generation = models.CharField(default='', max_length=15)

    def __str__(self):
        return f'{self.make} {self.model} {self.generation}'

class Categories(models.Model):
    """Model for categories which each product will have"""
    category = models.CharField(max_length=75)

    def __str__(self):
        return self.category

class Manufacturer(models.Model):
    """Manufacturer Name"""
    name = models.CharField(default='', max_length=100)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    """Model for each Product"""
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(default='', max_length=254)
    description = models.TextField()
    img = CloudinaryField('image')
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    ticket_price = models.DecimalField(max_digits=4, decimal_places=2)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_link = models.URLField(default='#')
    part_manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.part_manufacturer} {self.name}"

class Fitments(models.Model):
    """Bridge table to show ehich vehicles fit which products"""
    products = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f"{self.products} - {self.vehicle}"
