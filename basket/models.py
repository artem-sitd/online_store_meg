from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Reviews
from django.core import validators

# Вторая версия корзины*********************************************************************
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class ItemBasket(models.Model):
    cart = models.ForeignKey(Basket, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket_count = models.PositiveIntegerField(default=1, validators=[validators.MinValueValidator(0)])
    date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.cart} {self.product}'
