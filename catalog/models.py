from django.db import models


# Категории
class Category(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.title}'


# Подкатегория
class Subcategory(models.Model):
    title = models.CharField(max_length=40)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'



"""
Пока не сделал
"""
class Sales(models.Model):
    pass

class Banners(models.Model):
    pass

class ProductsPopular(models.Model):
    pass
class ProductsLimited(models.Model):
    pass