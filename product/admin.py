from django.contrib import admin
from .models import Product, Reviews, Specifications, ProductImage, Sales


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'price', 'count', 'rating', 'limited', 'category')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("author", 'product')


admin.site.register(Specifications)
admin.site.register(ProductImage)
admin.site.register(Sales)
