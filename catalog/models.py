from django.db import models

# путь хранения картинок категорий
def category_path(instance: 'CategoryImage', filename: str):
    return 'category/category_{pk}/images/{filename}'.format(pk=instance.category.pk, filename=filename)


# Категории
class Category(models.Model):
    title = models.CharField(max_length=40)
    subcategories = models.ForeignKey('self', on_delete=models.CASCADE,
                                      blank=True, null=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.title} ID = {self.id}'

# Картинки категорий
class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='image')
    src = models.ImageField(upload_to=category_path)
    alt = models.CharField(max_length=200, null=False, blank=True)

    # def __str__(self):
    #     return f'Image category:>>>  {self.category}'

"""
*********************************************** Пока не сделал ***********************************************
"""


class Sales(models.Model):
    pass


class Banners(models.Model):
    pass


class ProductsPopular(models.Model):
    pass


class ProductsLimited(models.Model):
    pass
