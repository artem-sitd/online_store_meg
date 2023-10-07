from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

"""
Product, Category1, Category2, Order, Profile, Basket, Reviews 
"""


# Путь хранения превью товаров
def product_preview(instance: 'Product', filename) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(pk=instance.pk, filename=filename)


# Модель товаров
class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    ordering = ['name']
    name = models.CharField(max_length=20, db_index=True)  # Название товара
    description = models.TextField(null=False, blank=True, db_index=True)  # Описание товара
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)  # Цена товара
    discount = models.SmallIntegerField(default=0)  # Скидка
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    archive = models.BooleanField(default=False)  # Архив
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, )  # Кем создан товар
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview)  # Превью товара (картинка)

    def __str__(self):
        return f'Product pk={self.pk} name={self.name!r}'

    # def get_absolute_url(self):
    #     return reverse('shop:products_detail', kwargs={'pk':self.pk})


# Модель заказов
class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)  # Адрес доставки
    promo = models.CharField(max_length=20, blank=True, null=False)  # Проомокод
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # Пользователь
    products = models.ManyToManyField(Product, related_name='orders')  # Перечень продуктов

    # def get_absolute_url(self):
    #     return reverse('shop:order_details', kwargs={'pk':self.pk})


# Путь хранения изобр. товаров
def product_path(instance: 'ProductImage', filename: str):
    return 'products/product_{pk}/images/{filename}'.format(pk=instance.product.pk, filename=filename)


# Модель картинок товаров
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_path)
    description = models.CharField(max_length=200, null=False, blank=True)


# Большая категория
class Category1(models.Model):
    name_category1 = models.CharField(max_length=40, on_delete=models.CASCADE)


# Вложенная категория
class Category2(models.Model):
    name_category1 = models.ForeignKey(Category1, on_delete=models.CASCADE)
    name_category2 = models.CharField(max_length=40)


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)  # Имя
    second_name = models.CharField(max_length=20, blank=True, null=True)  # Фамилия
    middle_name = models.CharField(max_length=20, blank=True, null=True)  # Отчество
    telephone = models.CharField(max_length=12, blank=True, null=True)  # Телефон
    email = models.EmailField(max_length=50)  # Почта
    birthday = models.DateTimeField(blank=True, null=True)  # Дата рождения
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar)


# Путь хранения аватара пользователя
def avatar(instance: 'Profile', filename) -> str:
    return 'avatars/avatar_{pk}/{filename}'.format(pk=instance.pk, filename=filename)

# Отзывы
class Reviews(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

# Корзина
class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
