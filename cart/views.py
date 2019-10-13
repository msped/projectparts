from django.shortcuts import render, redirect, reverse

# Create your views here.

def view_cart(request):
    """Renders the cart view"""
    return render(request, 'cart.html')

def add_to_cart(request, product_id):
    """Adds specified quantity of a product into the cart"""

    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] = int(cart[product_id]) + quantity
    else:
        cart[product_id] = cart.get(product_id, quantity)

    request.session['cart'] = cart
    return redirect(reverse('home'))

def update_cart(request, product_id):
    """Updates cart contents"""

    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)

    return redirect(reverse('view_cart'))
