from django.shortcuts import render
from .models import Product

# Create your views here.
def products_view(request):
    """Shows all products"""
    products = Product.objects.filter()

    return render(request, 'products.html', {'products': products})
