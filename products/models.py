from django.db import models

# Create your models here.

class Categories(models.Model):
    """Model for categories which each product will have"""
    category = models.CharField(max_length=75)

    def __str__(self):
        return self.category 

class Product(models.Model):
    """Model for each Product"""
    name = models.CharField(default='', max_length=254)
    description = models.TextField()
    img = models.ImageField(default='default.jpg', upload_to='media')
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    ticket_price = models.DecimalField(max_digits=4, decimal_places=2)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name