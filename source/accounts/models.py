from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Token(models.Model):
    token = models.UUIDField(verbose_name='token', default=uuid4)
    user = models.ForeignKey('auth.User', related_name='registration_tokens',
                             verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token)


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    about_user = models.TextField(null=True, blank=True, verbose_name='О себе')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



