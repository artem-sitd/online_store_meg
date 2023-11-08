from product.models import Product
from .serializers import BasketApiSerialize
from .models import ItemBasket, TestBasket
from rest_framework.views import APIView
from rest_framework.response import Response


class BasketApi(APIView):
    def get(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id)  # Определяем корзину с привязкой к юзеру >>> pwd123
        qs = ItemBasket.objects.prefetch_related('product').filter(cart_id=user_cart.id)
        serialized2 = BasketApiSerialize(qs, many=True)
        return Response(data=serialized2.data, status=200)

    # Добавление продукта
    def post(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id)
        product = Product.objects.get(id=request.data['id'])
        items_in_basket = ItemBasket.objects.prefetch_related('product').filter(cart=user_cart.id)
        if items_in_basket.filter(product__id=request.data['id']).exists():
            temp = items_in_basket.get(product=product)
            temp.basket_count += request.data['count']
            temp.save()
            serialized = BasketApiSerialize(items_in_basket, many=True)
            return Response(data=serialized.data, status=200)
        else:
            data = ItemBasket.objects.create(cart=user_cart, product=product,
                                             basket_count=request.data['count'])
            serialized = BasketApiSerialize(data)
            return Response(data=serialized.data, status=200)

    # Удаление продукта из корзины
    def delete(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id)
        product = Product.objects.get(id=request.data['id'])
        item_change = ItemBasket.objects.filter(cart=user_cart.id).get(product=product.id)

        if request.data['count'] >= item_change.basket_count:
            item_change.delete()
            serialized = BasketApiSerialize(product)
            return Response(data=serialized.data, status=200)
        item_change.basket_count -= request.data['count']
        item_change.save()
        serialized = BasketApiSerialize(item_change)
        return Response(data=serialized.data, status=200)
