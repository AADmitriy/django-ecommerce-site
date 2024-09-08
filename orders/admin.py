from django.contrib import admin

from .models import AvailableForShippingRegion, OrderAddress, OrderContact, PayCheck, Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(OrderAddress)
admin.site.register(OrderContact)
admin.site.register(Order, OrderAdmin)
admin.site.register(PayCheck)
admin.site.register(AvailableForShippingRegion)