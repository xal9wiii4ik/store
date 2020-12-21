from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Пользователь профиля')
    phone = models.CharField(max_length=25, blank=True, verbose_name='Телефон пользователя')
    address = models.CharField(max_length=60, blank=True, verbose_name='Адресс пользователя')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания пользователя')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Обновление пользователя')
    is_shop = models.BooleanField(default=False, verbose_name='Является ли магазином')
    legal_address = models.CharField(max_length=60, blank=True, verbose_name='Юридический адресс магазина')
    unp = models.CharField(max_length=60, blank=True, verbose_name='Унп магазина')
    bank_detail = models.CharField(max_length=60, blank=True, verbose_name='Детали связанные с банком')

    def __str__(self):
        return f"{self.user.username}, id: {self.id}"
