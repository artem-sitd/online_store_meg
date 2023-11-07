from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from product.models import Product
from rest_framework.response import Response
from rest_framework.request import Request
import random

# api/categories (первый вариант)
class CategoryListApi(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        parent = Category.objects.filter(parent_id=None)
        return parent


# class CategoryListApi(APIView):
#     def get(self, request:Request):
#         q_data = Category.objects.filter(parent_id=None)
#         serialized = CategorySerializer(q_data, many=True)
#         return Response(data=serialized.data, status=200)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': int(self.get_page_number(self.request, self.page_size)),
            'lastPage': self.page.paginator.num_pages
        })


# Все продукты с использованием сериализатора
class ProductApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer


class LimitedProductsApiView(APIView):
    def get(self, request):
        data = Product.objects.filter(limited=True)
        serialized = ProductSerializer(data, many=True)
        return Response(serialized.data, status=200)


class BannersApiView(APIView):
    def get(self, request):
        data=random.sample(list(Product.objects.all()), 3)
        print(data)
        serialized=ProductSerializer(data, many=True)
        return Response(serialized.data, status=200)