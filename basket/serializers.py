from rest_framework import serializers
from tags.models import Tags
from .models import Basket
from product.models import Product, Reviews, ProductImage

# для ProductSerializer
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author',)

# для ProductSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt')

# для ProductSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')

# для BasketSerializer
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True)
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description', 'free_delivery',
                  'images', 'tags', 'reviews', 'rating')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Basket
        fields = ('product',)
