from django.shortcuts import render, redirect
from django.views import View
import stripe
from cart.cart import Cart
from .forms import AddressForm, OrderContactForm
from django.conf import settings
from django.http import JsonResponse
from .models import OrderAddress, PayCheck, Order
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from decimal import Decimal
import math

# Create your views here.
class PaymentPage(View):
    def get(self, request):
        user = request.user
        cart = Cart(request)
        address_form = AddressForm(initial={'country': 'Ukraine'})
        if user.is_authenticated:
            contact_form = OrderContactForm(initial={'firstname': user.first_name, 'lastname': user.last_name,
                                                     'email': user.email})
            user_addresses = user.orderaddress_set.all()
        else:
            contact_form = OrderContactForm()
            user_addresses = None
        
        cart_products_price = cart.get_total_price()
        shipping_price = Decimal("10.94")
        amount = round(shipping_price + cart_products_price, 2)

        host = request.get_host()

        paypal_form_info = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': amount,
            'item_name': 'Sunpower Commerce Order ',
            'invoice': '',
            'currency_code': 'USD',
            'notify_url': 'http://' + host + f"{reverse('paypal-ipn')}",
            'return_url': 'http://' + host + f"{reverse('success_paypal')}",
            'cancel_url': 'http://' + host + f"{reverse('cancel')}",
        }

        paypal_form = PayPalPaymentsForm(initial=paypal_form_info)


        context = {
            'cart_products_price': cart.get_total_price(),
            'shipping_price': shipping_price,
            'total_price': amount,
            'address_form': address_form,
            'contact_form': contact_form,
            'paypal_form': paypal_form,
            'user': user,
            'user_addreses': user_addresses,
        }
    
        return render(request, 'orders/payment_page.html', context)

    def post(self, request):
        cart = Cart(request)
        address_form = AddressForm(request.POST)
        contact_form = OrderContactForm(request.POST)

        if not address_form.is_valid(): return JsonResponse({'errors': address_form.errors})
        if not contact_form.is_valid(): return JsonResponse({'errors': address_form.errors})

        cart_obj = cart.save_to_db()
        shipping_address = address_form.save()
        order_contacts = contact_form.save()

        payment_method = request.POST.get('card-choice')

        shipping_price = Decimal("10.94")
        total_products_price = Decimal(cart.get_total_price())
        amount = round(shipping_price + total_products_price, 2)

        pay_check = PayCheck.objects.create(amount=amount, payment_method=payment_method)
        order = Order.objects.create(address=shipping_address, cart=cart_obj,
                                     contact=order_contacts, paycheck=pay_check,
                                     shipping_price=shipping_price, total_price=amount)

        host = request.get_host()

        return self.process_payment(payment_method, order, host)


    def process_payment(self, payment_method, order, host):
        if payment_method == 'stripe':
            return self.process_stripe_payment(order, host)
        elif payment_method == 'paypal':
            return JsonResponse({'order_id': order.id})

    def process_stripe_payment(self, order, host):
        cart = order.cart

        cart_items = []

        for cart_item in cart.cartitem_set.all():
            cart_item_info = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': cart_item.product.title
                    },
                    'unit_amount_decimal': cart_item.product.price * 100,
                },
                'quantity': cart_item.quantity
            }
            cart_items.append(cart_item_info)

        shipping_info = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Delivery',
                },
                'unit_amount_decimal': order.shipping_price * 100
            },
            'quantity': 1
        }
        cart_items.append(shipping_info)
        
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        session = stripe.checkout.Session.create(
            line_items = cart_items,
            mode = 'payment',
            success_url = "http://" + host + '/orders/success_stripe?session_id={CHECKOUT_SESSION_ID}&' + f'order_id={order.id}',
            cancel_url = "http://" + host + '/orders/cancel',
        )

        return redirect(session.url, code=303)


def success_paypal(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(pk=order_id)
    if order.status == 'UNPAID':
        return redirect(cancel_page)

    return render(request, 'orders/success_page.html')

def success_stripe(request):
    checkout_session_id = request.GET.get('session_id', None)
    order_id = request.GET.get('order_id')

    order = Order.objects.get(id=order_id)

    paycheck = order.paycheck
    paycheck.paid = True
    paycheck.checkout_id = checkout_session_id
    paycheck.save()

    order.status='PENDING'
    order.save()

    return render(request, 'orders/success_page.html')

def cancel_page(request):
    return render(request, 'orders/cancel_page.html')

