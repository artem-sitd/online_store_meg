from rest_framework import serializers
from .models import Product, Reviews, Specifications, Tags, ProductImage


# Инфо о всех отзывах конкретного продукта
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author', 'email', 'text', 'rate', 'date')


# ProductDetailSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt')


# api/product/id/reviews
class ReviewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author', 'email', 'text', 'rate', 'date')


# ProductDetailSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


# ProductDetailSerializer
class SpecificSerialize(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = ('name', 'value')


# api/product/id
class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewsDetailSerializer(many=True)
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)
    specifications = SpecificSerialize()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'fullDescription', 'free_delivery', 'images', 'tags', 'reviews', 'specifications', 'rating',)
