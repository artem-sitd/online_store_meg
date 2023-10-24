from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from product.models import Product


class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Все продукты с использованием сериализатора
class ProductApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

