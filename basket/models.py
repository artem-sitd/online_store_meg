from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Reviews
from django.core import validators

# Корзина
class Basket(models.Model):
    product = models.ManyToManyField(Product, related_name='basket_product')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    basket_count=models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])
    def __str__(self):
        return f'Basket user >>> {self.user} <<<'
