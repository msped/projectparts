from django.contrib.auth.models import User
from products.models import Product
from cart.models import OrderItem
from cart.contexts import cart_contents
from checkout.models import Entries

def add_session_items_to_db(request):
    """Function that adds users session cart to database"""
    cart = request.session.get('cart', {})
    user = User.objects.get(id=request.user.id)
    for key, value in cart.items():
        product = Product.objects.get(id=int(key))
        new_order = OrderItem.objects.create(
            user=user,
            product=product,
            quantity=int(value)
        )
        new_order.save()
    request.session['cart'] = cart
    cart_contents(request)

def get_users_orders(orders):
    """get all users orders and place in list"""
    users_orders = []
    for item in orders:
        order_answer = item.user_answer_correct
        entries_per_order = []
        entries = Entries.objects.filter(order=item.id)
        for ent in entries:
            entries_per_order.append(ent.ticket_number)
        order_total = item.quantity * item.product.ticket_price
        order_to_add = [
            item,
            order_total,
            order_answer,
            entries_per_order
        ]

        users_orders.append(order_to_add)

    return users_orders
