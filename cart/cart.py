from shop.models import Product
from decimal import Decimal
from django.conf import settings
from shop.serializers import ProductSerializer
from . import models

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = request.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
    
    def __iter__(self):
        cart_products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=cart_products_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = ProductSerializer(product).data

        for item in cart.values():
            item['total_price'] = str(round(Decimal(item['price']) * item['quantity'], 2))
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_product(self, product_id):
        product_info = self.cart[str(product_id)].copy()
        product_info['total_price'] = str(round(Decimal(product_info['price']) * product_info['quantity'], 2))

        return product_info

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': 0,
            }
            
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def set_quantity(self, product_id, quantity):
        if str(product_id) not in self.cart:
            return False

        self.cart[str(product_id)]['quantity'] = quantity
        self.save()

        return True
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
        

    def save(self):
        self.session.modified = True

    def save_to_db(self, user=None):
        db_cart = models.Cart.objects.create(user=user)

        for product_id, product_info in self.cart.items():
            models.CartItem.objects.create(product_id=product_id, quantity=product_info['quantity'], cart=db_cart)

        return db_cart

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return round(sum(Decimal(item['price']) * item['quantity'] 
                   for item in self.cart.values()), 2)
    
   