from django.contrib.auth.models import User
from django.db import models


# Путь хранения аватара пользователя
def avatar(instance: "Profile", filename) -> str:
    return "avatars/avatar_user_pk_{pk}/{filename}".format(pk=instance.profile.user.pk, filename=filename)


# Профиль пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=20, blank=True, null=True)  # Имя
    phone = models.CharField(
        max_length=12, blank=True, null=True, default="+0123456789"
    )  # Телефон
    email = models.EmailField(max_length=50, default="example@mail.com")  # Почта

    def __str__(self: 'object of class Profile') -> str:
        return f"User: {self.user}, Fullname: {self.fullName}"


class Avatar(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="avatar", null=True, blank=True
    )
    src = models.ImageField(null=True, blank=True, upload_to=avatar)
    alt = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self: 'object of class Avatar') -> str:
        return f"src:{self.src}" f"alt:{self.alt}"
