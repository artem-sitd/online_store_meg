from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
from catalog.models import Category, Subcategory

# Сериализатор
# class ProductApiView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# Без сериализатора
# class ProductApiView(APIView):
#     def get(self, request: Request) -> Response:
#         products = Product.objects.all()
#         data = [{'name': i.name,
#                  'price': i.price,
#                  'category': Category.objects.get(id=i.category2.name_category1_id).name_category1,
#                  'subcategory': i.category2.name_category2,
#                  'description':i.description,
#                  'discount':i.discount,
#                  'created_at':i.created_at,
#                  'created_by':i.created_by.username} for i in products]
#         return Response({'Products': data})
