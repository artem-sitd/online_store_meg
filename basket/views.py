from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from product.models import Product, ProductImage, Reviews
from .serializers import BasketSerializer2, BasketApi3Serialize, BasketSerializer, ProductSerializer, BasketApi3Serialize
from .models import Basket, ItemBasket, TestBasket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, exceptions

# Первая версия*****************************************************************************
class BasketApi(ListCreateAPIView, DestroyAPIView):
    serializer_class = BasketSerializer
# # Первый вариант. Передаем модель корзины
    def get_queryset(self):
        basket_user = Basket.objects.filter(user=self.request.user.id).only('product')
        return basket_user

# Вторая версия*****************************************************************************
class BasketApi2(APIView):
    def get(self, request):
        basket = Basket.objects.all().prefetch_related('product').get(user=request.user.id).product.all()
        serialized = BasketSerializer2(basket, many=True)
        return Response(data=serialized.data, status=200)

# Третья версия через 2 модели**************************************************************
class BasketApi3(APIView):
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
        return Response(data=serialized.data, status=200)

        # говнокод>>>>>>> но рабочий
        # serialized=BasketApi3Serialize(product_instance) # Пытаемся сериализовать все поля объектов (выдает ошибку)
        # return Response(data=serialized.data, status=200)
        # j = [{'id': i.product_id,
        #       'category': Product.objects.get(id=i.product_id).category.title,
        #       'price': Product.objects.get(id=i.product_id).price,
        #       'count': ItemBasket.objects.filter(cart_id=user_cart.id).get(product_id=i.product_id).basket_count,
        #       'date': ItemBasket.objects.filter(cart_id=user_cart.id).get(product_id=i.product_id).date.strftime(
        #           '%a %b %d %Y %H:%M:%S') + ' GMT+0100 (Central European Standard Time)',
        #       'title': Product.objects.get(id=i.product_id).title,
        #       'description': Product.objects.get(id=i.product_id).description,
        #       'freeDelivery': Product.objects.get(id=i.product_id).free_delivery,
        #       'images': [{'src': k.src.url, 'alt': k.alt} for k in ProductImage.objects.filter(product=i.product_id)],
        #       'tags': [{'id': k.id, 'name': k.name} for k in
        #                Product.objects.prefetch_related('tags').get(id=i.product_id).tags.all()],
        #       'reviews': len(Reviews.objects.filter(product=i.product_id)),
        #       'rating': Product.objects.get(id=i.product_id).rating
        #       }
        #      for i in items_in_basket.all()]
        # return Response(j)

    # Добавление продукта
    def post(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id)
        product_id = Product.objects.get(id=request.data['id'])
        items_in_basket = ItemBasket.objects.filter(cart=user_cart.id)
        if items_in_basket.filter(product__id=request.data['id']).exists():
            raise exceptions.ParseError('Object already in basket')
        else:
            data = ItemBasket.objects.create(cart=user_cart, product=Product.objects.get(id=request.data['id']),
                                             basket_count=request.data['count'])
            serialized = BasketApi3Serialize(data.product)
            return Response(data=serialized.data, status=200)

    # Удаление продукта из корзины
    def delete(self, request):
        user_cart = TestBasket.objects.get(user=request.user.id)
        product_id = Product.objects.get(id=request.data['id'])
        items_in_basket = ItemBasket.objects.filter(cart=user_cart.id).get(product=product_id.id).delete()
        serialized = BasketApi3Serialize(product_id)
        return Response(data=serialized.data, status=200)
