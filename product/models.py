from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Category
from django.contrib.auth.models import User
from tags.models import Tags
from django.core.validators import MaxValueValidator


# Модель товаров
class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    ordering = ['name']
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)  # подкатегория
    title = models.CharField(max_length=20, db_index=True)  # Название товара
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)  # Цена товара
    count = models.IntegerField(default=5)  # Имеющееся кол-во
    date = models.DateTimeField(auto_now_add=True)  # Дата создания
    description = models.CharField(max_length=50, null=False, blank=True, db_index=True)  # Краткое Описание товара
    fullDescription = models.CharField(max_length=500, null=False, blank=True)  # Полное описание товара
    free_delivery = models.BooleanField(default=False)  # Бесплатная доставка
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=3.0,
                                 validators=[MaxValueValidator(5.0)])  # оценка
    specifications = models.ForeignKey('Specifications', on_delete=models.CASCADE, blank=True,
                                       null=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return f'{self.title}'

    # def get_absolute_url(self):
    #     return reverse('shop:products_detail', kwargs={'pk':self.pk})


def product_path(instance: 'ProductImage', filename: str):
    return 'products/product_{pk}/images/{filename}'.format(pk=instance.product.pk, filename=filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    src = models.ImageField(upload_to=product_path)
    alt = models.CharField(max_length=200, null=False, blank=True)


class Specifications(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}:{self.value}'


# Отзывы
class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    email = models.EmailField(max_length=50)
    rate = models.DecimalField(max_digits=2, decimal_places=1)  # оценка пользователя
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')

    def __str__(self):
        return f'{self.author}, {self.text[:50]}...'
