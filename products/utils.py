from .models import Vehicle

def get_makes():
    """Function to get all vehicle makes and remove duplicates"""
    cars = Vehicle.objects.all()

    makes = []
    for car in cars:
        if car.make not in makes:
            makes.append(car.make)
    return makes

def get_products_from_fitments(fitments):
    """Get products from fitments queryset"""
    products = []
    for prod in fitments:
        products.append(prod.products)
    return products

def get_sort_options(sort_options):
    """Get search options for results with vehicle"""
    if sort_options == "name":
        sort_by = 'products__name'
    elif sort_options == "-name":
        sort_by = '-products__name'
    elif sort_options == "ticket_price":
        sort_by = 'products__ticket_price'
    else:
        sort_by = '-products__ticket_price'
    return sort_by
