from django.db import models


# путь хранения картинок категорий
def category_path(instance: "CategoryImage", filename: str) -> str:
    return "category/category_{pk}/images/{filename}".format(
        pk=instance.category.pk, filename=filename
    )


# Категории
class Category(models.Model):
    title = models.CharField(max_length=40)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Родитель",
        related_name="subcategories",
    )

    def __str__(self:'object of class Category') -> str:
        return f"{self.title} ID = {self.id}"


# Картинки категорий
class CategoryImage(models.Model):
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="image"
    )
    src = models.ImageField(upload_to=category_path)
    alt = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self:'object of class CategoryImage') -> str:
        return f"Image category:>>>  {self.category}"
