from .serializers import BasketSerializer, BasketSerializer2
from .models import Basket
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


# class BasketApi(ListCreateAPIView, DestroyAPIView):
#     serializer_class = BasketSerializer
# # # Первый вариант. Передаем модель корзины
#     def get_queryset(self):
#         basket_user = Basket.objects.filter(user=self.request.user.id).only('product')
#         return basket_user
# #     # Добавление продукта в корзину
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#
#         print(request.user)
#         return self.create(request, *args, **kwargs)
# #     # Удаление продукта из корзины
#     def delete(self, request, *args, **kwargs):
#         print('def delete****************')
#         return self.destroy(request, *args, **kwargs)

class BasketApi(APIView):
    def get(self, request):
        basket = Basket.objects.all().prefetch_related('product').get(user=request.user.id).product.all()
        serialized = BasketSerializer2(basket, many=True)
        return Response(data=serialized.data, status=200)
