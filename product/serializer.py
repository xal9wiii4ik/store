from rest_framework import serializers

from product.models import (
    Category,
    Product,
    ProductImage,
    DesiredList
)


class CategoryModelSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категории"""

    class Meta:
        model = Category
        fields = '__all__'


class ProductImageModelSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели фотографии продукта"""

    image_url = serializers.CharField(source='image.url', read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'image_url']


class ProductModelSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели продукта"""

    price_with_discount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    images = ProductImageModelSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount',
                  'material', 'service_life', 'guarantee',
                  'description', 'user', 'category',
                  'price_with_discount', 'images', 'quantity']


class DesiredListModelSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка желаемого"""

    class Meta:
        model = DesiredList
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}
