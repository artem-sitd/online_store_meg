from collections import OrderedDict

import pytz
from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from basket.models import ItemBasket
from product.models import Product, ProductImage, Reviews
from tags.models import Tags


# для ProductSerializer
class ReviewsSerializer(serializers.Field):
    def get_attribute(self, instance: Product) -> Product:
        return instance

    def to_representation(self, instance) -> int:
        len_review = Reviews.objects.filter(product=instance.id)
        return len(len_review)


# для ProductSerializer
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


# для ProductSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name")


# для BasketSerializer*******************************************************************************
class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )
    date = SerializerMethodField()
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)
    reviews = ReviewsSerializer()
    rating = serializers.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=3.0,
        validators=[MaxValueValidator(5.0)],
        coerce_to_string=False,
    )
    freeDelivery = SerializerMethodField()

    def get_freeDelivery(self, obj: Product) -> str:
        return f"{obj.free_delivery}"

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_date(self, obj: Product) -> str:
        temp = obj.date.astimezone(pytz.timezone("CET"))
        return (
            temp.strftime("%a %b %d %Y %H:%M:%S")
            + " GMT+0100 (Central European Standard Time)"
        )


# для BasketApi
class BasketApiSerialize(serializers.ModelSerializer):
    product = ProductSerializer()
    count = serializers.SerializerMethodField()

    def get_count(self, obj: ItemBasket) -> str:
        return f"{obj.basket_count}"

    class Meta:
        model = ItemBasket
        fields = ("product", "count")

    def to_representation(self, instance: ItemBasket) -> OrderedDict:
        data = super().to_representation(instance)["product"]
        data["count"] = super().to_representation(instance)["count"]
        data["count"] = int(data["count"])
        return data
