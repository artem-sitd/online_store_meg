from django.urls import path
from .views import BasketApi, BasketApi2, BasketApi3



urlpatterns = [path('basket/', BasketApi3.as_view()), #для get
               path('basket', BasketApi3.as_view()), # для post
               ]
