from django.contrib import admin
from .models import Basket, ItemBasket, TestBasket

admin.site.register(Basket)
admin.site.register(ItemBasket)
admin.site.register(TestBasket)

