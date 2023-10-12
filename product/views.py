from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductReviewSerializer
from catalog.serializers import ProductSerializer
from .models import Product, Reviews
from catalog.models import Category


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Отзыв на конкретный товар
class ProductDetailReview(generics.ListAPIView):
    def get_queryset(self):
        self.list_review = Reviews.objects.filter(product_id=self.kwargs['pk'])
        return self.list_review

    serializer_class = ProductReviewSerializer
