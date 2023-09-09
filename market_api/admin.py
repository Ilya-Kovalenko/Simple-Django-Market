from django.contrib import admin

from .models import Product, Cart, CartList

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartList)
