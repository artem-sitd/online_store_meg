from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Reviews


# Корзина
class Basket(models.Model):
    product = models.ManyToManyField(Product, related_name='basket_product')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
