import pytz
from rest_framework import serializers

from auth_custom.models import Profile
from basket.models import Basket, ItemBasket
from catalog.serializers import ProductSerializer
from product.models import Product

from .models import Order


# Сериализация для GET api/order/id и api/orders
class OrderDetailSerialize(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    totalCost = serializers.SerializerMethodField()

    # Получение стоимости продуктов в заказе
    def get_totalCost(self, obj: Order) -> float:
        user_cart = Basket.objects.get(user=obj.user)
        items_cart = ItemBasket.objects.filter(cart=user_cart).values(
            "product", "basket_count"
        )
        total = 0
        for i in items_cart:
            total += Product.objects.get(id=i["product"]).price * i["basket_count"]
        return total

    def get_createdAt(self, obj: Order) -> str:
        temp = obj.createdAt.astimezone(pytz.timezone("CET"))
        return temp.strftime("%Y-%m-%d %H:%M")

    def get_fullName(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.user_id).fullName

    def get_email(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.user_id).email

    def get_phone(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.user_id).phone

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )
