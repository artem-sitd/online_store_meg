from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from product.models import Product

class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Все продукты с использованием сериализатора
class ProductApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer