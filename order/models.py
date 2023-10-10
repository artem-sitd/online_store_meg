from django.db import models
from product.models import Product
from django.contrib.auth.models import User

# Модель заказов
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # Пользователь
    product = models.ManyToManyField(Product, related_name='orders')  # Перечень продуктов

    # def get_absolute_url(self):
    #     return reverse('shop:order_details', kwargs={'pk':self.pk})
