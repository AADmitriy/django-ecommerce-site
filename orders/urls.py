from django.urls import path, include
from . import views


urlpatterns = [
    path('payment_page', views.PaymentPage.as_view(), name='payment_page'),
    path('success_paypal', views.success_paypal, name='success_paypal'),
    path('success_stripe', views.success_stripe, name='success_stripe'),
    path('cancel', views.cancel_page, name='cancel'),
]
