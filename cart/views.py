from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from competition.models import Competition
from products.models import Product
from .models import Orders

# Create your views here.

@login_required
def view_cart(request):
    """Renders the cart view"""
    try:
        orders = Orders.objects.filter(user=request.user.id)
    except Orders.DoesNotExist:
        orders = False
    return render(request, 'cart.html', {'orders': orders})

@login_required
def add_to_cart(request, product_id):
    """Adds specified quantity of a product into the cart"""

    quantity = int(request.POST.get('quantity'))

    comp = Competition.objects.get(is_active=True)

    order = Orders.objects.filter(
        user=request.user.id,
        related_competition=comp.id,
        product=product_id,
        is_paid=False
    )

    if order.exists():
        new_qty = order[0].quantity + quantity
        order.update(quantity=new_qty)
        messages.success(request, '{} tickets added to cart.'.format(quantity))
    else:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)
        new_order = Orders.objects.create(
            user=user,
            related_competition=comp,
            product=product,
            quantity=quantity
        )
        new_order.save()
        messages.success(request, '{} tickets added to cart.'.format(quantity))

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

    if qty == 0:
        order.delete()
    else:
        order.quantity = qty
        order.save()
    return redirect(reverse('view_cart'))

@login_required
def remove_item(request, order_id):
    """Remove an item from the cart"""
    order = Orders.objects.filter(id=order_id)
    order.delete()
    messages.error(request, 'Ticket(s) Removed.')

    return redirect(reverse('view_cart'))
