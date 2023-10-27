import pytz
from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Category, CategoryImage
from product.models import Product, ProductImage, Reviews, Tags


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
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('src', 'alt')


# ProductSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


# ProductSerializer (кол-во отзывов)
class ReviewsSerializer(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, instance):
        temp = Reviews.objects.filter(product=instance.id)
        return len(temp)


# api/catalog
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer()
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)
    price=serializers.DecimalField(max_digits=8, decimal_places=2, coerce_to_string=False)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, default=3.0,
                                 validators=[MaxValueValidator(5.0)], coerce_to_string=False)
    date=SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'free_delivery', 'images',  'tags', 'reviews', 'rating',)

    def get_date(self, obj):
        temp=obj.date.astimezone(pytz.timezone('CET'))
        return temp.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0100 (Central European Standard Time)'
