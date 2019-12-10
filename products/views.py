import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Categories, Manufacturer, Vehicle

# Create your views here.
def products_view(request):
    """Shows all products"""
    products = Product.objects.filter()
    cars = Vehicle.objects.all()
    manufacturer_dropdown = Manufacturer.objects.all()
    categories_dropdown = Categories.objects.all()

    makes = []
    for car in cars:
        if car.make not in makes:
            makes.append(car.make)

    make = request.GET.get('make')
    model = request.GET.get('model')
    generation = request.GET.get('generation')
    manufacturer = request.GET.get('manufacturer')
    categories = request.GET.get('categories')
    sort_options = request.GET.get('sort')

    if make and model and generation:
        cars = Vehicle.objects.get(
            make=make,
            model=model,
            generation=generation
        )
        if make and model and generation and manufacturer is None and categories is None:
            products = Product.objects.filter(
                fits=cars
            ).order_by(sort_options)
        elif manufacturer and categories is None:
            products = Product.objects.filter(
                fits=cars,
                part_manufacturer=manufacturer
            ).order_by(sort_options)
        elif categories and manufacturer is None:
            products = Product.objects.filter(
                fits=cars,
                category=categories
            ).order_by(sort_options)
        elif manufacturer and categories:
            products = Product.objects.filter(
                fits=cars,
                part_manufacturer=manufacturer,
                category=categories
            ).order_by(sort_options)
    else:
        if manufacturer and categories is None:
            products = Product.objects.filter(
                part_manufacturer=manufacturer
            ).order_by(sort_options)
        elif categories and manufacturer is None:
            products = Product.objects.filter(
                category=categories
            ).order_by(sort_options)
        elif manufacturer and categories:
            products = Product.objects.filter(
                part_manufacturer=manufacturer,
                category=categories
            ).order_by(sort_options)

    return render(request, 'products.html', {
        'products': products,
        'makes': makes,
        'manufacturer': manufacturer_dropdown,
        'categories': categories_dropdown
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
