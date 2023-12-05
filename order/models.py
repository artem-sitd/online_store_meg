from django.contrib.auth.models import User
from django.db import models

from product.models import Product


# Модель заказов
class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # Пользователь
    products = models.ManyToManyField(
        Product, related_name="orders"
    )  # Перечень продуктов
    deliveryChoice = (
        ("free", "free"),
        ("express", "express"),
        ("ordinary", "ordinary"),
    )
    paymentChoice = (("online", "online"), ("someone", "someone"))
    deliveryType = models.CharField(
        max_length=15, choices=deliveryChoice, default="free", blank=True, null=True
    )
    paymentType = models.CharField(
        max_length=15, choices=paymentChoice, default="online", blank=True, null=True
    )
    status = models.CharField(max_length=15, default="accepted", blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True, default="Moscow")
    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="Lenina street, 41, 310 apartment",
    )
    totalCost = models.DecimalField(
        default=0, decimal_places=2, max_digits=10, blank=True, null=True
    )

    def __str__(self:'object of class Order') -> str:
        return f"Order ID= {self.id}, User= {self.user}>>{self.products.all()}"
