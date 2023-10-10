from django.db import models

class Tags(models.Model):
    name=models.CharField(max_length=15)