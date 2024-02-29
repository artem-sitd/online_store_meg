import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from product.models import Product, ProductImage, Reviews, Sales, Tags

from .models import Category, CategoryImage


# CategorySerializer
class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ("src", "alt")


# CategorySerializer
class SubcategorySerialize(serializers.Field):
    def get_attribute(self, instance: Category) -> QuerySet:
        sub = Category.objects.filter(parent=instance)
        return sub

    def to_representation(self, value: QuerySet) -> list:
        list_value = []
        for subcategory in value:
            temp = {"id": subcategory.id, "title": subcategory.title}
            try:
                image = CategoryImage.objects.get(category=temp["id"])
                temp["image"] = {"src": image.src.url, "alt": image.alt}
            except ObjectDoesNotExist:
                temp["image"] = None
            list_value.append(temp)
        return list_value


# api/categories
class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()
    subcategories = SubcategorySerialize()

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")


# ProductSerializer******************************************************************************************
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


# ProductSerializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name")


# ProductSerializer (кол-во отзывов)
class ReviewsSerializer(serializers.Field):
    def get_attribute(self, instance: Product) -> Product:
        return instance

    def to_representation(self, instance: Product) -> int:
        temp = Reviews.objects.filter(product=instance.id)
        return len(temp)


# api/catalog
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer()
    images = ImagesSerializer(many=True)
    tags = TagsSerializer(many=True)
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
    date = SerializerMethodField()

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
            "free_delivery",
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


class SalesSerialized(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    salePrice = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj: Sales) -> list:
        qs = ProductImage.objects.filter(product=obj.product)
        images = list({"src": i.src.url, "alt": i.alt} for i in qs)
        return images

    def get_dateTo(self, obj: Sales) -> str:
        return obj.dateTo.strftime("%m-%d")

    def get_dateFrom(self, obj: Sales) -> str:
        return obj.dateFrom.strftime("%m-%d")

    def get_id(self, obj: Sales) -> int:
        return obj.product.id

    def get_price(self, obj: Sales) -> int:
        return obj.product.price

    def get_title(self, obj) -> str:
        return obj.product.title

    class Meta:
        model = Sales
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "images")
