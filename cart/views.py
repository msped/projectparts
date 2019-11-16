from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from competition.models import Competition
from products.models import Product
from .models import Orders

# Create your views here.

def view_cart(request):
    """Renders the cart view"""
    return render(request, 'cart.html')

def add_to_cart(request, product_id):
    """Adds specified quantity of a product into the cart"""

    quantity = int(request.POST.get('quantity'))

    comp = Competition.objects.get(is_active=True)
    user = User.objects.get(id=request.user.id)

    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        order = Orders(
            user=user,
            related_competition=comp,
            product=product,
            quantity=quantity
        )
        order.save()
        return redirect(reverse('products'))
    else:
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] = int(cart[product_id]) + quantity
        else:
            cart[product_id] = cart.get(product_id, quantity)

        request.session['cart'] = cart
        return redirect(reverse('products'))

def update_cart(request, product_id):
    """Updates cart contents"""

    quantity = int(request.POST.get('quantity'))

    if request.user.is_authenticated:
        comp = Competition.objects.get(is_active=True)
        order = Orders.objects.get(
            user=request.user.id,
            related_competition=comp.id,
            product=product_id,
            is_paid=False
        )
        if quantity > 0:
            order.quantity = quantity
            order.save()
        else:
            order.delete()
    else:
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id)

        return redirect(reverse('products'))
