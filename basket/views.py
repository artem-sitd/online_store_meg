from product.models import Product
from .serializers import ProductSerializer, BasketApiSerialize
from .models import ItemBasket, TestBasket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

# Третья версия через 2 модели**************************************************************
class BasketApi(APIView):
    # Полученеи продуктов в корзине
    def get(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id) # Определяем корзину с
                                                                    # привязкой к юзеру >>> pwd123

        items_in_basket = ItemBasket.objects.prefetch_related('product')\
            .filter(cart_id=user_cart.id).values_list('product', flat=True) #Определяем перечень продуктов в корзине.
                                                        # Выдает объекты модели ItemBasket >>> <QuerySet [4, 2]>
        product_instance=Product.objects.filter(id__in=items_in_basket) # Получаем объекты !!конкретно!! модели Product (список из id)
                                    # на выходе кортеж из объектов Product
                                    # >>>> <QuerySet [<Product: Call of duty 2, id=2>, <Product: Elden Ring, id=4>]>
        serialized=ProductSerializer(product_instance, many=True)

        # Сериализация через BasketApiSerialize
        qs=ItemBasket.objects.prefetch_related('product').filter(cart_id=user_cart.id)
        serialized2=BasketApiSerialize(qs, many=True)
        return Response(data=serialized2.data, status=200)
        # return Response(data=serialized.data, status=200)

    # Добавление продукта
    def post(self, request):
        # НЕОБХОДИМО ПЕРЕДАВАТЬ НЕ ПРОДУКТЫ, А ВСЕ ОБЪЕКТЫ ItemBasket, ЧТОБЫ ДОБРАТЬСЯ ДО ПРАВИЛЬНОГО COUNT!!
        user_cart = TestBasket.objects.get(user=request.user.id)
        product = Product.objects.get(id=request.data['id'])
        items_in_basket = ItemBasket.objects.filter(cart=user_cart.id)
        if items_in_basket.filter(product__id=request.data['id']).exists():
            raise exceptions.ParseError('Object already in basket')
        else:
            data = ItemBasket.objects.create(cart=user_cart, product=product,
                                             basket_count=request.data['count'])
            serialized = ProductSerializer(data.product)
            return Response(data=serialized.data, status=200)

    # Удаление продукта из корзины
    def delete(self, request):
        #НУЖНО ПЕРЕДЕЛАТЬ ЛОГИКУ УДАЛЕНИЯ, СРАВНИВАЯ COUNT ИЗ REQUEST.DATA['COUNT'] И BASKET_COUNT
        # ПРИ УМНЕЬШЕНИИ УОЛИЧЕСТВА - НЕ НАДО УДАЛЯТЬ ВЕСЬ ПРОДУКТ!!!!
        print(request.data)
        user_cart = TestBasket.objects.get(user=request.user.id)
        product = Product.objects.get(id=request.data['id'])
        ItemBasket.objects.filter(cart=user_cart.id).get(product=product.id).delete()
        serialized = BasketApiSerialize(product)
        return Response(data=serialized.data, status=200)
