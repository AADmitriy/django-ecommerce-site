from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('product_page/<product_id>/', views.product_page, name='product_page'),
    path('api/products', views.ProductsApi.as_view()),
]