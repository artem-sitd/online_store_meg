from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator


class Payment(models.Model):
    name = models.CharField(max_length=50)  # Имя фамилия владельца карты
    number = models.CharField(max_length=8, validators=[MinLengthValidator(8)])  # Номер карты только 8 символов
    month_tuple = (('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'),
                   ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'))
    month = models.CharField(default='01', choices=(month_tuple), max_length=2)  # месяц
    year = models.IntegerField(default=2000, validators=[MinValueValidator(2000), MaxLengthValidator(4)])
    code = models.CharField(default='000', validators=[MinLengthValidator(3)],
                            max_length=3)  # cvv карты. Больше проверок пока не сделал
