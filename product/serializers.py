from django.core.validators import MaxValueValidator
from rest_framework import serializers

from .models import Product, ProductImage, Reviews, Specifications, Tags


# Инфо о всех отзывах конкретного продукта
class ProductReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ("author", "email", "text", "rate", "date")

    def get_author(self, obj: Reviews) -> str:
        return obj.author.username

    def get_date(self, obj: Reviews) -> str:
        return obj.date.strftime("%Y-%m-%d %H:%M")


# ProductDetailSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


# ProductDetailSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name")


# ProductDetailSerializer
class SpecificSerialize(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = ("name", "value")


# api/product/id
class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ProductReviewSerializer(many=True)
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)
    specifications = SpecificSerialize(many=True)
    price = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )
    rating = serializers.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=3.0,
        validators=[MaxValueValidator(5.0)],
        coerce_to_string=False,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "free_delivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )
