from django.urls import path
from .views import BasketApi, BasketApi2, BasketApi3



urlpatterns = [path('basket/', BasketApi.as_view()),
               path('basket2/', BasketApi2.as_view()),
               path('basket3/', BasketApi3.as_view()),

               ]
