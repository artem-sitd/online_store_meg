from django.contrib import admin

from .models import Basket, ItemBasket

admin.site.register(ItemBasket)
admin.site.register(Basket)
