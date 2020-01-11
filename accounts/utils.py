from django.contrib.auth.models import User
from products.models import Product
from competition.models import Competition
from cart.models import Orders
from cart.contexts import cart_contents

def add_session_items_to_db(request):
    """Function that adds users session cart to database"""
    cart = request.session.get('cart', {})
    user = User.objects.get(id=request.user.id)
    for key, value in cart.items():
        product = Product.objects.get(id=int(key))
        comp = Competition.objects.get(is_active=True)
        new_order = Orders.objects.create(
            user=user,
            related_competition=comp,
            product=product,
            quantity=int(value)
        )
        new_order.save()
    request.session['cart'] = cart
    cart_contents(request)
