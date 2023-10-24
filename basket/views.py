from .serializers import BasketSerializer
from .models import Basket
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404


class BasketListApi(ListCreateAPIView, DestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    # Получение списка продуктов в корзине
    def get_object(self):
        return get_object_or_404(Basket, user=self.request.user)

    # Добавление продукта в корзину
    def post(self, request, *args, **kwargs):
        id_poduct = request.id
        count_product = request.count
        return self.create(request, *args, **kwargs)

    # Удаление продукта из корзины
    def delete(self, request, *args, **kwargs):
        id_poduct = request.id
        count_product = request.count
        return self.destroy(request, *args, **kwargs)
