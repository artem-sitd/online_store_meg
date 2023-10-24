from rest_framework import generics
from .serializers import ProductReviewSerializer
from catalog.serializers import ProductDetailSerializer
from .models import Product, Reviews


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# Отзыв на конкретный товар
class ProductDetailReview(generics.ListAPIView):
    def get_queryset(self):
        self.list_review = Reviews.objects.filter(product_id=self.kwargs['pk'])
        return self.list_review

    serializer_class = ProductReviewSerializer
