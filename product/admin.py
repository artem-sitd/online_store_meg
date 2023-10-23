from django.contrib import admin
from .models import Product, Reviews, Specifications, ProductImage

admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(Specifications)
admin.site.register(ProductImage)