from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Orders

def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    if request.user.is_authenticated:
        cart_items = []
        total = 0
        product_amount = 0

        try:
            cart_tickets = Orders.objects.filter(user=request.user.id, is_paid=False)
        except Orders.DoesNotExist:
            return None
        for item in cart_tickets:
            product = get_object_or_404(Product, pk=item.id)
            total += product.ticket_price
            product_amount += 1
            cart_items.append({
                'id': product.id,
                'total': total,
                'product_amount': product_amount
            })

        return {
            'cart_items': cart_items,
            'total': total,
            'product_count': product_amount
        }

    else:
        cart = request.session.get('cart', {})

        cart_items = []
        total = 0
        product_amount = 0

        for id, quantity in cart.items():
            product = get_object_or_404(Product, pk=id)
            total += quantity * product.price
            product_amount += quantity
            cart_items.append({
                'id': id,
                'quantity': quantity,
                'product': product
            })

        return {
            'cart_items': cart_items,
            'total': total,
            'product_count': product_amount
        }
    