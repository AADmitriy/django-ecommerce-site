from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Category, Product
from django.core.exceptions import FieldError
from .load_items import load_categories, load_products

# Create your views here.

def main_page(request):
    products = Product.objects.all().order_by('-date')
    categories = Category.objects.all()

    if not categories.exists(): 
        load_categories()
        categories = Category.objects.all()
    
    if not products.exists():
        load_products()
        products = Product.objects.all().order_by('-date')

    context = {"products": products,
               "categories": categories,}
    

    return render(request, 'shop/main_page.html', context)


def product_page(request, product_id):
    product = Product.objects.get(id=product_id)

    if not product.left_in_storage > 0:
        return render(request, 'shop/runout_of_product.html')

    context = {
        "product": product,
    }

    return render(request, 'shop/product_page.html', context)


class ProductsApi(APIView):
    def get(self, request):
        if not request.query_params:
           products = Product.objects.all()
           serializer = ProductSerializer(products, many=True)
    
           return Response(serializer.data)

        params = request.query_params
        if not self.is_valid_params(params): return Response({'error': 'Invalid parameters'})

        try:
            products = self.select_products(params)
        except (FieldError, ValueError):
             return Response({'error': 'Invalid parameters'})

        serializer = ProductSerializer(products, many=True)
    
        return Response(serializer.data)
    
    
    def select_products(self, params):
        name_like = params['name_like'] if 'name_like' in params else ''
        if 'sort_by' in params:
            products = Product.objects.filter(title__icontains=name_like).order_by(params['sort_by'])
        else:
            products = Product.objects.filter(title__icontains=name_like)

        for key, value in params.items():
            if 'category' == key:
                products = [product for product in products if value in product.categories_list]
            if 'min_price' == key:
                products = [product for product in products if product.price >= int(value)]
            if 'max_price' == key:
                products = [product for product in products if product.price <= int(value)]

        return products
        
    
    def is_valid_params(self, query_params):
        allowed_params = ['category', 'min_price', 'max_price', 'sort_by', 'name_like']

        for key in query_params:
            if key not in allowed_params:
                return False

        return True
