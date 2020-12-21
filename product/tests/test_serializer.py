from django.contrib.auth.models import User
from django.db.models import F
from django.test import TestCase

from product.models import Category, Product
from product.serializer import CategoryModelSerializer, ProductModelSerializer


class CategorySerializerTestCase(TestCase):
    """Тест для сериалайзера категории"""

    def test_ok(self):
        """Тест для проверки валидации сериалайзера категории"""

        category = Category.objects.create(name='category')
        category_1 = Category.objects.create(name='category_1')

        categories = Category.objects.all()
        data = CategoryModelSerializer(categories, many=True).data

        expected_data = [
            {
                'id': 1,
                'name': 'category'
            },
            {
                'id': 2,
                'name': 'category_1'
            }
        ]
        self.assertEqual(expected_data, data)


class ProductSerializerTestCase(TestCase):
    """Тест для сериалайзера продуктов"""

    def test_ok(self):
        """Тест для проверки валидации сериалайзера продуктов"""

        user = User.objects.create(username='user',
                                   is_active=True,
                                   is_staff=True)
        user_1 = User.objects.create(username='user_1',
                                     is_active=True)
        category = Category.objects.create(name='category')
        category_1 = Category.objects.create(name='category_1')

        product = Product.objects.create(name='product',
                                         price='22.00',
                                         discount='10.00',
                                         material='material',
                                         service_life=2,
                                         guarantee=1,
                                         description='description',
                                         user=user,
                                         category=category)
        product_1 = Product.objects.create(name='product_1',
                                           price='10.00',
                                           material='material_1',
                                           description='description_1',
                                           user=user_1,
                                           category=category_1)

        products = Product.objects.all().annotate(
            price_with_discount=F('price')-F('discount')
        )
        data = ProductModelSerializer(products, many=True).data

        expected_data = [
            {
                'id': 1,
                'name': 'product',
                'price': '22.00',
                'discount': '10.00',
                'material': 'material',
                'service_life': 2,
                'guarantee': 1,
                'description': 'description',
                'user': user.id,
                'category': category.id,
                'price_with_discount': '12.00',
                'images': []
            },
            {
                'id': 2,
                'name': 'product_1',
                'price': '10.00',
                'discount': '0.00',
                'material': 'material_1',
                'service_life': 0,
                'guarantee': 0,
                'description': 'description_1',
                'user': user_1.id,
                'category': category_1.id,
                'price_with_discount': '10.00',
                'images': []
            }
        ]
        self.assertEqual(expected_data, data)
