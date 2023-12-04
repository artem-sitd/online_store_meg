from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_custom.models import Profile
from basket.models import Basket, ItemBasket
from product.models import Product

from .models import Order
from .serializers import OrderDetailSerialize


# api/orders Предварительное оформление заказа
class OrdersApiView(APIView):
    # api/orders
    def get(self, request: Request) -> Response:
        data = Order.objects.filter(user=request.user)
        serialized = OrderDetailSerialize(data, many=True)
        return Response(data=serialized.data, status=200)

    # По нажатию на оформить заказ возвращает orderId. Сначала post, потом get
    def post(self, request: Request) -> Response:
        user_cart = Basket.objects.get(
            user=request.user.id
        )  # Определение корзины юзера
        items_in_basket = ItemBasket.objects.filter(cart=user_cart.id)
        products_list = Product.objects.filter(
            id__in=items_in_basket.values_list("product", flat=True)
        )
        data = Order.objects.create(user=request.user)
        data.products.set(products_list)
        data.save()
        return Response(data={"orderId": data.id}, status=200)


# api/orders/id уточнение заказа
class OrdersDetailApiView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        order_id = self.kwargs["id"]
        serialized = OrderDetailSerialize(Order.objects.get(id=order_id))
        return Response(serialized.data, status=200)

    def post(self, request: Request, **kwargs) -> Response:
        order_id = self.kwargs["id"]
        current_order = Order.objects.get(id=order_id)
        change_profile = Profile.objects.get(user=current_order.user)
        current_order.deliveryType = request.data["deliveryType"]
        current_order.paymentType = request.data["paymentType"]
        current_order.city = request.data["city"]
        current_order.address = request.data["address"]

        # Суть такая: если при оформлении заказа пользователь изменил данные,
        # относящиеся к профилю, тогда эти изменения будут также вноситься в его профиль
        change_profile.phone = request.data["phone"]  # Выполнить изменения в профиль
        change_profile.fullName = request.data[
            "fullName"
        ]  # Выполнить изменения в профиль.

        current_order.save()
        return Response({"orderId": current_order.id}, status=200)
