from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from competition.models import Competition
from products.models import Product
from .models import Orders

# Create your views here.

@login_required
def view_cart(request):
    """Renders the cart view"""
    orders = Orders.objects.filter(user=request.user.id)
    return render(request, 'cart.html', {'orders': orders})

@login_required
def add_to_cart(request, product_id):
    """Adds specified quantity of a product into the cart"""

    quantity = int(request.POST.get('quantity'))

    comp = Competition.objects.get(is_active=True)

    user = User.objects.get(id=request.user.id)
    product = Product.objects.get(id=product_id)
    order = Orders.objects.get_or_create(
        user=user,
        related_competition=comp,
        product=product,
        quantity=quantity
    )
    order.save()
    return redirect(reverse('products'))

@login_required
def increase_item(request, order_id):
    """increases cart item by one"""
    order = Orders.objects.get(id=order_id)

    qty = int(order.quantity) + 1

    order.quantity = qty
    order.save()
    return redirect(reverse('view_cart'))

@login_required
def decrease_item(request, order_id):
    """decreases cart item by one"""
    order = Orders.objects.get(id=order_id)

    qty = int(order.quantity) - 1

    order.quantity = qty
    order.save()
    return redirect(reverse('view_cart'))

@login_required
def remove_item(request, order_id):
    """Remove an item from the cart"""

    order = Orders.objects.filter(id=order_id)
    order.delete()

    return redirect(reverse('view_cart'))
