from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Orders

def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    cart_items = []
    total = 0
    product_amount = 0
    cart = request.session.get('cart', {})
    if request.user.is_authenticated:
        try:
            cart = Orders.objects.filter(
                user=request.user.id,
                is_paid=False
            )
        except cart.DoesNotExist:
            return None
        for item in cart:
            product = get_object_or_404(Product, pk=item.product_id)
            total += product.ticket_price * item.quantity
            product_amount += 1
            cart_items.append({
                'id': item.id,
                'quantity': item.quantity,
                'product': product
            })
    else:

        for id, quantity in cart.items():
            product = get_object_or_404(Product, pk=id)
            total += quantity * product.ticket_price
            product_amount += 1
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
