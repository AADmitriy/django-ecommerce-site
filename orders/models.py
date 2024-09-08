from django.db import models
from cart.models import Cart
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AvailableForShippingRegion(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class OrderAddress(models.Model):
    country = models.ForeignKey(AvailableForShippingRegion, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True)
    address= models.CharField(max_length=256)
    zipCode = models.IntegerField()
    city = models.CharField(max_length=256)
    

class OrderContact(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    phoneNumber = models.IntegerField()
    email = models.CharField(max_length=256)


class PayCheck(models.Model):
    amount = models.DecimalField(max_digits=64, decimal_places=2)
    payment_method = models.CharField(max_length=128)
    checkout_id = models.CharField(max_length=512, default=None, null=True)
    payer_id = models.CharField(max_length=150, default=None, null=True)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True)


class Order(models.Model):
    address = models.ForeignKey(OrderAddress, on_delete=models.SET_NULL, default=None, null=True)
    contact = models.ForeignKey(OrderContact, on_delete=models.SET_NULL, default=None, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, default=None, null=True)
    paycheck = models.ForeignKey(PayCheck, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    shipping_price = models.DecimalField(max_digits=64, decimal_places=2)
    total_price = models.DecimalField(max_digits=64, decimal_places=2)

    class StatusEnum(models.TextChoices):
        UNPAID = 'UNPAID', _('Unpaid')
        PENDING = 'PENDING', _('Pending')
        DELIVERING = 'DELIVERING', _('Delivering')
        DELIVERED = 'DELIVERED', _('Delivered')

    status = models.CharField(
        max_length=10,
        choices=StatusEnum.choices,
        default=StatusEnum.UNPAID,
    )
