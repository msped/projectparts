from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from competition.models import Competition
from products.models import Product
from .contexts import cart_contents
from .models import Orders

# Create your views here.

def view_cart(request):
    """Renders the cart view"""
    return render(request, 'cart.html')

def add_to_cart(request):
    """Adds specified quantity of a product into the cart"""

    if request.method == "POST":
        quantity = int(request.POST.get('qty'))
        product_id = int(request.POST.get('product_id'))

        if request.user.is_authenticated:
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
        else:
            cart = request.session.get('cart', {})
            if product_id in cart:
                cart[product_id] = int(cart[product_id]) + quantity
            else:
                cart[product_id] = cart.get(product_id, quantity)

            request.session['cart'] = cart

    cart_amount = cart_contents(request)

    data = {
        'cart_amount': cart_amount['product_count']
    }

    return JsonResponse(data)

def increase_item(request, order_id):
    """increases cart item by one"""

    if request.user.is_authenticated:
        order = Orders.objects.get(id=order_id)
        if order.is_paid is False:
            qty = int(order.quantity) + 1
            order.quantity = qty
            order.save()
    else:
        cart = request.session.get('cart', {})
        print(cart)
        cart[order_id] = int(cart[order_id]) + 1
        request.session['cart'] = cart
    cart_total = cart_contents(request)

    data = {
        'qty': qty,
        'total': cart_total['total']
    }

    return JsonResponse(data)

def decrease_item(request, order_id):
    """decreases cart item by one"""
    if request.user.is_authenticated:
        order = Orders.objects.get(id=order_id)
        if order.is_paid is False:
            qty = int(order.quantity) - 1
            order.quantity = qty
            order.save()
    else:
        cart = request.session.get('cart', {})
        cart[order_id] = int(cart[order_id]) - 1
        qty = cart[order_id]
        request.session['cart'] = cart
    cart_total = cart_contents(request)

    data = {
        'qty': qty,
        'total': cart_total['total']
    }

    return JsonResponse(data)

def remove_item(request, order_id):
    """Remove an item from the cart"""
    if request.user.is_authenticated:
        order = Orders.objects.filter(id=order_id)
        order.delete()
        messages.error(request, 'Ticket(s) Removed.')
    else:
        cart = request.session.get('cart', {})
        cart.pop(order_id)
        request.session['cart'] = cart

    return redirect(reverse('view_cart'))
