from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Subcategory
from django.contrib.auth.models import User
from tags.models import Tags


# Модель товаров
class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    ordering = ['name']
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)  # подкатегория
    title = models.CharField(max_length=20, db_index=True)  # Название товара
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)  # Цена товара
    count = models.IntegerField(default=5)  # Имеющееся кол-во
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    description = models.CharField(max_length=50, null=False, blank=True, db_index=True)  # Краткое Описание товара
    fullDescription = models.CharField(max_length=500, null=False, blank=True)  # Полное описание товара
    free_delivery = models.BooleanField(default=False)  # Бесплатная доставка
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # оценка
    specifications = models.ForeignKey('Specifications', on_delete=models.SET_DEFAULT, default='not chosen')
    reviews = models.ForeignKey('Reviews', on_delete=models.SET_DEFAULT, default='not chosen' )
    tags = models.ForeignKey(Tags, on_delete=models.SET_DEFAULT, default='not chosen')

    def __str__(self):
        return {self.title}

    # def get_absolute_url(self):
    #     return reverse('shop:products_detail', kwargs={'pk':self.pk})


class Specifications(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)


# Отзывы
class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    email = models.EmailField(max_length=50)
    rate = models.DecimalField(max_digits=2, decimal_places=1)  # оценка пользователя
    date = models.DateTimeField(auto_now_add=True)
