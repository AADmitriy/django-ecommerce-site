from django.contrib import admin

from .models import CartItem, Cart

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

class CartItemAdmin(admin.ModelAdmin):
    list_filter = [
        ("cart_id", admin.RelatedOnlyFieldListFilter),
    ]

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
