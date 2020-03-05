from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import get_makes, get_products_from_fitments, get_sort_options
from .models import Product, Categories, Manufacturer, Vehicle, Fitments

# Create your views here.
def products_view(request):
    """Shows all products"""
    products = Product.objects.all()
    manufacturer_dropdown = Manufacturer.objects.all()
    categories_dropdown = Categories.objects.all()

    makes = get_makes()

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
        sort_options = get_sort_options(request.GET.get('sort'))
        if make and model and generation and manufacturer is None and categories is None:
            fitments = Fitments.objects.filter(
                vehicle=cars
            ).order_by(sort_options)
            products = get_products_from_fitments(fitments)
        elif manufacturer and categories is None:
            fitments = Fitments.objects.filter(
                vehicle=cars,
                products__part_manufacturer=manufacturer
            ).order_by(sort_options)
            products = get_products_from_fitments(fitments)
        elif categories and manufacturer is None:
            fitments = Fitments.objects.filter(
                vehicle=cars,
                products__category=categories
            ).order_by(sort_options)
            products = get_products_from_fitments(fitments)
        elif manufacturer and categories:
            fitments = Fitments.objects.filter(
                vehicle=cars,
                products__part_manufacturer=manufacturer,
                products__category=categories
            ).order_by(sort_options)
            products = get_products_from_fitments(fitments)
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

    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products_paginator = paginator.get_page(page)

    return render(request, 'products.html', {
        'products': products_paginator,
        'makes': makes,
        'manufacturer': manufacturer_dropdown,
        'categories': categories_dropdown
    })

def product_detail(request, product_id):
    """Shows extra detail on a product"""
    product = Product.objects.get(id=product_id)
    fits = Fitments.objects.filter(products=product)

    car_product_fits = []
    for item in fits:
        car_product_fits.append(item.vehicle)

    return render(request, 'product_detail.html',
                  {'product': product, 'fits': car_product_fits})

def get_models(request):
    """Get Models from Make"""
    if request.method == "POST":
        make = request.POST['make']
        models_db = Vehicle.objects.filter(make=make)

        models = []
        for model in models_db:
            models.append(model.model)

    return JsonResponse(models, safe=False)

def get_gens(request):
    """Get Generations from Make and Model"""
    if request.method == "POST":
        make = request.POST['make']
        model = request.POST['model']
        gens_db = Vehicle.objects.filter(make=make, model=model)

        gens = []
        for gen in gens_db:
            gens.append(gen.generation)

    return JsonResponse(gens, safe=False)
