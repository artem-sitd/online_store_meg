from rest_framework import serializers
from .models import Product, Reviews

# Инфо о всех отзывах конкретного продукта
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author', 'email', 'text', 'rate', 'date')


