from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self: 'object of class Tags') -> str:
        return f"{self.name}"
