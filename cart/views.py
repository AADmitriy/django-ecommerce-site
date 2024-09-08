from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shop.models import Product
from .cart import Cart

# Create your views here.
def payment_page(request):
    return render(request, 'cart/payment_page.html')

@api_view()
def cart_detail(request):
    cart = Cart(request)
    
    return Response(cart)

@api_view()
def cart_get_product(request, product_id):
    cart = Cart(request)

    return Response(cart.get_product(product_id))

@api_view()
def cart_get_total_quantity(request):
    cart = Cart(request)

    return Response(cart.get_total_quantity())

@api_view(['POST'])
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)

    return Response({'success': 'true'})

@api_view(['POST'])
def cart_set_item_quantity(request, product_id, quantity):
    cart = Cart(request)
    success = cart.set_quantity(product_id=product_id, quantity=quantity)

    return Response({'success': success})

@api_view(['POST'])
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)

    return Response({'success': 'true'})
