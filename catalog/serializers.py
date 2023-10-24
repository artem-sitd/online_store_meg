from rest_framework import serializers
from .models import Category, CategoryImage
from product.models import Product, ProductImage, Reviews, Tags, Specifications


# CategorySerializer
class SubcategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


# CategorySerializer
class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ('src', 'alt')

# api/categories
class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer
    subcategories = SubcategorySerialize()
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

# ProductSerializer
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author',)


# ProductSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt')


# ProductSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


# api/catalog
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True)
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'fullDescription', 'images', 'free_delivery', 'tags', 'reviews', 'rating',)


# api/product/id/reviews
class ReviewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('author', 'email', 'text', 'rate', 'date')


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
