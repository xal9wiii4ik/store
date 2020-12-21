import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_unique_image_url(name, image_name):
    """Получение уникальной ссылки на фотографию"""

    time = timezone.now().strftime("%d-%m-%Y-%H-%S.%f")[:-4]
    image_extension = image_name.split('.')[-1]
    rename = name + time + '.' + image_extension
    return os.path.join(rename)


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(max_length=60, unique=True, verbose_name='Название категории')

    def __str__(self):
        return f'{self.id}, {self.name}'


class Product(models.Model):
    """Модель продуктов"""

    name = models.CharField(max_length=60, verbose_name='Название продукта')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена продукта')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Скидка на продукт')
    material = models.CharField(max_length=60, verbose_name='Материал продукта')
    service_life = models.PositiveIntegerField(default=0, verbose_name='Срок службы продукта')
    guarantee = models.PositiveIntegerField(default=0, verbose_name='Гарантия продукта')
    description = models.TextField(max_length=255, verbose_name='Описание продукта')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Владелец продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория продукта')
    quantity = models.BigIntegerField(verbose_name='Количество на складе')

    def __str__(self):
        return f'{self.name}, {self.material}, {self.user}, {self.service_life}, {self.id}, {self.quantity}'


class ProductImage(models.Model):
    """Модель фотографии продукта"""

    image = models.ImageField(upload_to='products_images', verbose_name='Фотография продукта')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='images')

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = get_unique_image_url(self.product.name, self.image.name)
        return super().save(*args, **kwargs)


class DesiredList(models.Model):
    """Модель списка желаемого"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Владелец списка')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')
