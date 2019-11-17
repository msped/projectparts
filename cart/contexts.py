from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Orders

def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    cart = []
    total = 0
    product_amount = 0

    try:
        cart_items = Orders.objects.filter(user=request.user.id, is_paid=False)
    except cart_items.DoesNotExist:
        return None
    for item in cart_items:
        product = get_object_or_404(Product, pk=item.product_id)
        total += product.ticket_price * item.quantity
        product_amount += 1
        cart.append({
            'id': product.id,
            'total': total,
            'product_amount': product_amount
        })

    return {
        'cart_items': cart,
        'total': total,
        'product_count': product_amount
    }
