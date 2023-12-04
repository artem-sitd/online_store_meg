import random
from collections import Counter, OrderedDict

from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Reviews, Sales

from .models import Category
from .serializers import CategorySerializer, ProductSerializer, SalesSerialized


# api/categories
class CategoryListApi(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self) -> QuerySet:
        parent = Category.objects.filter(parent_id=None)
        return parent


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data: OrderedDict) -> Response:
        return Response(
            {
                "items": data,
                "currentPage": int(self.get_page_number(self.request, self.page_size)),
                "lastPage": self.page.paginator.num_pages,
            }
        )


class ProductApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductSerializer

    # Для сортировок на странице каталога, но оно не меняет на странице
    def get_queryset(self) -> list | QuerySet:
        if self.request.query_params["sort"] == "reviews":
            data = (
                Product.objects.get(id=i[0])
                for i in sorted(
                    dict(
                        Counter(
                            Reviews.objects.prefetch_related("product")
                            .all()
                            .values_list("product", flat=True)
                        )
                    ).items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            )
            data = [i for i in data]
            return data
        queryset = Product.objects.all().order_by(self.request.query_params["sort"])
        return queryset


class LimitedProductsApiView(APIView):
    def get(self, request: Request) -> Response:
        data = Product.objects.filter(limited=True)
        serialized = ProductSerializer(data, many=True)
        return Response(serialized.data, status=200)


class BannersApiView(APIView):
    def get(self, request: Request) -> Response:
        data = random.sample(list(Product.objects.all()), 3)
        serialized = ProductSerializer(data, many=True)
        return Response(serialized.data, status=200)


class SalesApiView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Sales.objects.prefetch_related("product").all().order_by("-id")
    serializer_class = SalesSerialized


class PopularApiView(APIView):
    # Выборка по количеству отзывов
    def get(self, request: Request) -> Response:
        data = (
            Reviews.objects.prefetch_related("product")
            .all()
            .values_list("product", flat=True)
            .order_by("id")
        )
        popular_list = list(i[0] for i in Counter(data).most_common(4))
        serialized = ProductSerializer(
            Product.objects.filter(id__in=popular_list), many=True
        )
        return Response(serialized.data, status=200)
