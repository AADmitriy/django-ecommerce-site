from django.shortcuts import get_object_or_404
from .models import Order
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver
from django.conf import settings


@receiver(valid_ipn_received)
def valid_payment_notification(sender, **kwargs):
    ipn = sender
    print('Valid IPN recieved')
    if ipn.payment_status == 'Completed':
        order = get_object_or_404(Order, id=ipn.invoice)
        if order.total_price == ipn.mc_gross and settings.PAYPAL_RECEIVER_EMAIL == ipn.receiver_email:
            paycheck = order.paycheck
            paycheck.paid = True
            paycheck.payer_id = ipn.payer_id
            paycheck.save()
        
            order.status='PENDING'
            order.save()

@receiver(invalid_ipn_received)
def invalid_payment_notification(sender, **kwargs):
    ipn = sender
    print('Invalid IPN recieved')
    if ipn.payment_status == 'Completed':
        order = get_object_or_404(Order, id=ipn.invoice)
        if order.total_price == ipn.mc_gross and settings.PAYPAL_RECEIVER_EMAIL == ipn.receiver_email:
            paycheck = order.paycheck
            paycheck.paid = True
            paycheck.payer_id = ipn.payer_id
            paycheck.save()
        
            order.status='PENDING'
            order.save()
