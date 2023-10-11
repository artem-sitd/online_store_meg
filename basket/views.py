from django.shortcuts import render
from .serializers import BasketSerializer
from rest_framework.generics import ListAPIView
from .models import Basket


class BasketListApi(ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
