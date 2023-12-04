from django.contrib import admin

from .models import Category, CategoryImage

admin.site.register(CategoryImage)


@admin.register(Category)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent")
