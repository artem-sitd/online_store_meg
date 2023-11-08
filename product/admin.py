from django.contrib import admin
from .models import Product, Reviews, Specifications, ProductImage, Sales

admin.site.register(Product)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("author", 'product')
admin.site.register(Specifications)
admin.site.register(ProductImage)
admin.site.register(Sales)