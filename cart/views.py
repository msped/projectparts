from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon
from products.models import Product
from competition.models import Competition
from .contexts import cart_contents
from .models import OrderItem, Order

# Create your views here.

def view_cart(request):
    """Renders the cart view"""
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        try:
            order = Order.objects.get(user=user, ordered=False)
            context = {'order': order}
        except Order.DoesNotExist:
            context = {}
    return render(request, 'cart.html', context)

def add_to_cart(request):
    """Adds specified quantity of a product into the cart"""

    if request.method == "POST":
        quantity = int(request.POST.get('qty'))
        product_id = request.POST.get('product_id')

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            product = Product.objects.get(id=product_id)
            comp = Competition.objects.get(is_active=True)

            order_item, created = OrderItem.objects.get_or_create(
                defaults={
                    'quantity': quantity
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
                    order_item.quantity = quantity
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
            data = {
                'qty': qty,
                'total': Order.objects.get(
                    user_id=request.user.id,
                    ordered=False).get_total()
            }
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
        orderitem = OrderItem.objects.get(id=order_id)
        if orderitem.is_paid is False:
            qty = int(orderitem.quantity) - 1
            orderitem.quantity = qty
            orderitem.save()
            data = {
                'qty': qty,
                'total': Order.objects.get(
                    user_id=request.user.id,
                    ordered=False).get_total()
            }
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

@csrf_exempt
def remove_item(request):
    """Remove an item from the cart"""
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        if request.user.is_authenticated:
            order_item = OrderItem.objects.get(
                id=order_id
            )
            order = Order.objects.get(
                user=request.user,
                ordered=False
            )
            order.items.remove(order_item)
            order_item.delete()
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

def add_coupon(request):
    """Adds Coupon to Order"""
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(user=user, ordered=False)
    if request.method == "POST":
        coupon_code = request.POST['coupon_code']
        validity_test = validate_coupon(coupon_code=coupon_code, user=user)
        if validity_test['valid']:
            coupon = Coupon.objects.get(code=coupon_code)
            order.coupon = coupon
            order.save()
            messages.success(request, "Coupon has been added to cart.")
            return redirect('view_cart')
        else:
            messages.error(
                request,
                "There was an error applying the coupon code."
            )
            return redirect('view_cart')
    else:
        return redirect('view_cart')

def remove_coupon(request):
    """Remove Coupon Code from Order"""
    user = User.objects.get(id=request.user.id)
    order = Order.objects.get(user=user, ordered=False)
    order.coupon = None
    order.save()
    messages.error(request, "Coupon code removed.")
    return redirect('view_cart')
