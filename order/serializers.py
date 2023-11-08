import pytz
from .models import Order
from product.models import Product
from catalog.serializers import ProductSerializer
from rest_framework import serializers
from auth_custom.models import Profile
from basket.models import ItemBasket, Basket


# вроде нигде не используется удалить в конце
class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'product')


# api/orders
class OrdersListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    createdAt = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_fullName(self, obj):
        profile = Profile.objects.get(user=obj.user)
        info = (profile.fullName, profile.email, profile.phone)
        return info

    def get_createdAt(self, obj):
        temp = obj.date.astimezone(pytz.timezone('CET'))
        return temp.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0100 (Central European Standard Time)'

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType',
                  'paymentType', 'totalCost', 'status', 'city', 'address', 'product')


# Сериализация для GET api/order/id
class OrderDetailSerialize(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    totalCost = serializers.SerializerMethodField()

    # Получение стоимости продуктов в заказе
    def get_totalCost(self, obj):
        user_cart = Basket.objects.get(user=obj.user)
        items_cart = ItemBasket.objects.filter(cart=user_cart).values('product', 'basket_count')
        total = 0
        for i in items_cart:
            total += Product.objects.get(id=i['product']).price * i['basket_count']
        return total

    def get_createdAt(self, obj):
        temp = obj.createdAt.astimezone(pytz.timezone('CET'))
        return temp.strftime("%Y-%m-%d %H:%M")

    def get_fullName(self, obj):
        return Profile.objects.get(user=obj.user_id).fullName

    def get_email(self, obj):
        return Profile.objects.get(user=obj.user_id).email

    def get_phone(self, obj):
        return Profile.objects.get(user=obj.user_id).phone

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType',
                  'totalCost', 'status', 'city', 'address', 'products')

