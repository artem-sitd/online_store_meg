from django.urls import path
from .views import BasketListApi

urlpatterns = [path('basket/', BasketListApi.as_view())

               ]
