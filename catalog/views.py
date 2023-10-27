from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from product.models import Product
from rest_framework.response import Response


class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
