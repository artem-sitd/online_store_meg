from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Reviews
from .serializers import ProductDetailSerializer, ProductReviewSerializer


# api/catalog
class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# Оставить отзыв
class ProductDetailReview(APIView):
    def post(self, request: Request, **kwargs) -> Response:
        email = request.data["email"]
        text = request.data["text"]
        rate = request.data["rate"]
        product_id = Product.objects.get(id=kwargs["pk"])
        data = Reviews.objects.create(
            product=product_id, author=request.user, text=text, rate=rate, email=email
        )
        serialized = ProductReviewSerializer(data)
        return Response(data=serialized.data, status=200)
