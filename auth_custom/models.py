from django.db import models
from django.contrib.auth.models import User


# Путь хранения аватара пользователя
def avatar(instance: 'Profile', filename) -> str:
    return 'avatars/avatar_{pk}/{filename}'.format(pk=instance.pk, filename=filename)


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=20, blank=True, null=True)  # Имя
    phone = models.CharField(max_length=12, blank=True, null=True)  # Телефон
    email = models.EmailField(max_length=50)  # Почта
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar)

    def __str__(self):
        return f'User: {self.user}, Fullname: {self.fullName}'
