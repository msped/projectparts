from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from products.models import Product
from .contexts import cart_contents
from .models import OrderItem

# Create your views here.

def view_cart(request):
    """Renders the cart view"""
    return render(request, 'cart.html')

def add_to_cart(request):
    """Adds specified quantity of a product into the cart"""

    if request.method == "POST":
        quantity = int(request.POST.get('qty'))
        product_id = request.POST.get('product_id')

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            product = Product.objects.get(id=product_id)

            order, created = OrderItem.objects.get_or_create(
                defaults={
                    'quantity': quantity
                },
                user=user,
                product=product,
                is_paid=False
            )

            if not created:
                new_qty = order.quantity + quantity
                order.quantity = new_qty
                order.save()
        else:
            cart = request.session.get('cart', {})
            if product_id in cart:
                p_id = str(product_id)
                cart[p_id] = int(cart[p_id]) + quantity
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
        order = OrderItem.objects.get(id=order_id)
        if order.is_paid is False:
            qty = int(order.quantity) + 1
            order.quantity = qty
            order.save()
    else:
        cart = request.session.get('cart', {})
        cart[order_id] = int(cart[order_id]) + 1
        qty = cart[order_id]
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
        order = OrderItem.objects.get(id=order_id)
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

def remove_item(request):
    """Remove an item from the cart"""
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        if request.user.is_authenticated:
            order = OrderItem.objects.filter(id=order_id)
            order.delete()
        else:
            cart = request.session.get('cart', {})
            cart.pop(order_id)
            request.session['cart'] = cart

    cart_total = cart_contents(request)

    data = {
        'total': cart_total['total'],
        'cart_amount': cart_total['product_count']
    }

    return JsonResponse(data)
