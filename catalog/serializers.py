from rest_framework import serializers
from .models import Category
from product.models import Product, Reviews

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Инфо о всех продуктов (не используется)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'fullDescription', 'free_delivery', 'tags', 'specifications', 'rating', )