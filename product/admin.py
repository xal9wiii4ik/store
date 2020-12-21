import logging

from django.contrib import admin
from django.utils.safestring import mark_safe

from product.models import (
    Category,
    Product,
    ProductImage,
    DesiredList
)


class ProductImagesInlineAdmin(admin.StackedInline):
    """Создание фотографии продукта инлайн вместе с продуктом"""

    model = ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий продукта"""

    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для продукта"""

    inlines = [ProductImagesInlineAdmin]
    list_display = ('id', 'name', 'price', 'discount',
                    'material', 'service_life', 'guarantee',
                    'description', 'user', 'category', 'quantity')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Админка для фотографий продукта"""

    def get_product_id(self, obj):
        """Получение айди продукта"""

        return obj.product.id

    def get_image(self, obj):
        """Вывод фотографии"""

        return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" />')

    list_display = ('id', 'product', 'get_image', 'get_product_id')


@admin.register(DesiredList)
class DesiredListAdmin(admin.ModelAdmin):
    """Админка для списка желаемых продуктов"""

    list_display = ('id', 'product', 'user')
