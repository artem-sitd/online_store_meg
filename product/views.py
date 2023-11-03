from rest_framework import generics
from rest_framework.views import APIView
from .serializers import ProductReviewSerializer, ProductDetailSerializer
from .models import Product, Reviews
from rest_framework.response import Response


# api/catalog
class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# Оставить отзыв
class ProductDetailReview(APIView):
    def post(self, request, **kwargs):
        email = request.data['email']
        text = request.data['text']
        rate = request.data['rate']
        product_id = Product.objects.get(id=kwargs['pk'])
        data = Reviews.objects.create(product=product_id, author=request.user, text=text, rate=rate, email=email)
        serialized = ProductReviewSerializer(data)
        return Response(data=serialized.data, status=200)
