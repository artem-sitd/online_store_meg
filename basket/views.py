from .serializers import BasketSerializer
from .models import Basket
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404


class BasketApi(ListCreateAPIView, DestroyAPIView):
    # queryset = Basket.objects.all().order_by('-date')
    serializer_class = BasketSerializer

    def get_queryset(self):
        return Basket.objects.filter(product=self.request.user.id)

    # Получение списка продуктов в корзине
    # def get_object(self):
    #     return get_object_or_404(Basket, user=self.request.user)

    # Добавление продукта в корзину
    def post(self, request, *args, **kwargs):
        print(request.data)

        print(request.user)
        return self.create(request, *args, **kwargs)

    # Удаление продукта из корзины
    def delete(self, request, *args, **kwargs):
        print('def delete****************')
        return self.destroy(request, *args, **kwargs)
