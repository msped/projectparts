from django.shortcuts import render
from .models import Product

# Create your views here.
def products_view(request):
    """Shows all products"""
    products = Product.objects.filter()

    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    """Shows extra detail on a product"""
    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {'product': product})
