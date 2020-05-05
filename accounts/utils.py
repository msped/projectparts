from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
from competition.models import Competition
from cart.models import OrderItem, Order
from cart.contexts import cart_contents
from checkout.models import Entries

def add_session_items_to_db(request):
    """Function that adds users session cart to database"""
    cart = request.session.get('cart', {})
    user = User.objects.get(id=request.user.id)
    comp = Competition.objects.get(is_active=True)
    for key, value in cart.items():
        product = Product.objects.get(id=int(key))
        order_item, created = OrderItem.objects.get_or_create(
            defaults={
                'quantity': int(value)
            },
            user=user,
            product=product,
            is_paid=False
        )
        order_qs = Order.objects.filter(
            user=user,
            ordered=False
        )

        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(pk=order_item.id).exists():
                order_item.quantity = int(value)
                order_item.save()
            else:
                order.items.add(order_item)
        else:
            order = Order.objects.create(
                user=user,
                related_competition=comp,
                order_date=timezone.now()
            )
            order.items.add(order_item)
            order.save()

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
