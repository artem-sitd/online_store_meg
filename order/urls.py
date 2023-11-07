from django.urls import path
from .views import OrdersApiView, OrdersDetailApiView

urlpatterns = [path('orders', OrdersApiView.as_view()),
               path('order/<int:id>', OrdersDetailApiView.as_view()),

               ]
