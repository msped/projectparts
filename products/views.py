import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Categories, Manufacturer, Vehicle

# Create your views here.
def products_view(request):
    """Shows all products"""
    products = Product.objects.filter()
    cars = Vehicle.objects.all()
    manufacturer = Manufacturer.objects.all()
    categories = Categories.objects.all()

    makes = []
    for car in cars:
        if car.make not in makes:
            makes.append(car.make)

    return render(request, 'products.html', {
        'products': products,
        'makes': makes,
        'manufacturer': manufacturer,
        'categories': categories
    })

def product_detail(request, product_id):
    """Shows extra detail on a product"""
    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {'product': product})

def get_models(request):
    """Get Models from Make"""
    make = request.POST['make']
    models_db = Vehicle.objects.filter(make=make)

    models = []
    for m in models_db:
        models.append(m.model)

    return HttpResponse(json.dumps(models), content_type="application/json")

def get_gens(request):
    """Get Generations from Make and Model"""
    make = request.POST['make']
    model = request.POST['model']
    gens_db = Vehicle.objects.filter(make=make, model=model)

    gens = []
    for g in gens_db:
        gens.append(g.generation)

    return HttpResponse(json.dumps(gens), content_type="application/json")
