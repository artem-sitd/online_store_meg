from django.urls import path
from .views import BasketApi



urlpatterns = [path('basket/', BasketApi.as_view()),

               ]
