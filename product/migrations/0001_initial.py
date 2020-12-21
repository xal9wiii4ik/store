# Generated by Django 3.1.3 on 2020-11-26 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Название категории')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Название продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена продукта')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Скидка на продукт')),
                ('material', models.CharField(max_length=60, verbose_name='Материал продукта')),
                ('service_life', models.PositiveIntegerField(default=0, verbose_name='Срок службы продукта')),
                ('guarantee', models.PositiveIntegerField(default=0, verbose_name='Гарантия продукта')),
                ('description', models.TextField(max_length=255, verbose_name='Описание продукта')),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='product.category', verbose_name='Категория продукта')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец продукта')),
            ],
        ),
    ]
