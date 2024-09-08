from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'date', 'main_img_url', 'main_img_webp_url']

    def get_price(self, product):
        return {
          'price': str(product.price),
          'type': 'Decimal',
        }
