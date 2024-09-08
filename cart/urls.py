from django.urls import path
from . import views


urlpatterns = [
    path('api_cart_detail', views.cart_detail),
    path('api_cart_get_product/<int:product_id>/', views.cart_get_product),
    path('api_cart_add/<int:product_id>/', views.cart_add),
    path('api_cart_remove/<int:product_id>/', views.cart_remove),
    path('api_cart_set_quantity/<int:product_id>/<int:quantity>', views.cart_set_item_quantity),
    path('api_cart_get_total_quantity', views.cart_get_total_quantity),
]
