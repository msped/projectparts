from django.contrib.auth.models import User
from products.models import Product
from cart.models import OrderItem, Order
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
        orderitems = []
        order_answer = item.answer_correct
        order_items = item.items.all()
        for ticket in order_items:
            order_item_current = OrderItem.objects.get(id=ticket.id)
            entries_per_order = []
            if order_answer:
                entries = Entries.objects.filter(orderItem=order_item_current.id)
                for ent in entries:
                    entries_per_order.append(ent.ticket_number)

            product_item = [
                ticket.product,
                ticket.quantity,
                entries_per_order
            ]
            orderitems.append(product_item)

        order_to_add = [
            item,
            Order.get_total(item),
            order_answer,
            [orderitems]
        ]
        users_orders.append(order_to_add)
    return users_orders
