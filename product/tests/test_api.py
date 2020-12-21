import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product.models import Product, Category
from product.serializer import ProductModelSerializer, CategoryModelSerializer
from user_profile.models import UserProfile


class CategoryApiTestCase(APITestCase):
    """Апи тесты для категорий"""

    def setUp(self):
        password = make_password('password')
        url = reverse('auth_path:token')

        self.user = User.objects.create(username='user',
                                        password=password,
                                        is_active=True,
                                        is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = 'Token ' + self.client.post(path=url,
                                                 data=json_data,
                                                 content_type='application/json').data['access']
        self.user_1 = User.objects.create(username='user_1',
                                          password=password,
                                          is_active=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = 'Token ' + self.client.post(path=url,
                                                   data=json_data_1,
                                                   content_type='application/json').data['access']

        self.category = Category.objects.create(name='category')
        self.category_1 = Category.objects.create(name='category_1')

    def test_get(self):
        """Тест для получения списка категорий"""

        url = reverse('category-list')
        categories = Category.objects.all()
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg='Im msg')
        self.assertEqual(CategoryModelSerializer(categories, many=True).data,
                         response.data)

    def test_create_staff(self):
        """Тест для создания категории администратором"""

        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-list')
        data = {
            'name': 'create_category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Category.objects.all().count())

    def test_create_staff_exist_name(self):
        """Тест для создания категории администратором
        существующее имя категории"""

        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-list')
        data = {
            'name': 'category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, Category.objects.all().count())

    def test_create_not_staff(self):
        """Тест для создания категории пользователем"""

        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-list')
        data = {
            'name': 'create_category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Category.objects.all().count())

    def test_update_staff(self):
        """Тест для обновления категории администратором"""

        self.assertEqual('category_1', self.category_1.name)
        url = reverse('category-detail', args=(self.category_1.id,))
        data = {
            'name': 'update_category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category_1.refresh_from_db()
        self.assertEqual('update_category', self.category_1.name)

    def test_update_staff_exist_name(self):
        """Тест для обновления категории администратором
        существующее имя категории"""

        self.assertEqual('category_1', self.category_1.name)
        url = reverse('category-detail', args=(self.category_1.id,))
        data = {
            'name': 'category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_not_staff(self):
        """Тест для обновления категории пользователем"""

        self.assertEqual('category_1', self.category_1.name)
        url = reverse('category-detail', args=(self.category_1.id,))
        data = {
            'name': 'update_category'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_staff(self):
        """Тест для удаления категории администратором"""

        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-detail', args=(self.category_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Category.objects.all().count())

    def test_delete_not_staff(self):
        """Тест для удаления категории пользователем"""

        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-detail', args=(self.category_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Category.objects.all().count())



class ProductApiTestCase(APITestCase):
    """Апи тесты для продуктов"""

    def setUp(self):
        password = make_password('password')
        url = reverse('auth_path:token')

        self.user = User.objects.create(username='user',
                                        password=password,
                                        is_active=True,
                                        is_staff=True)
        self.user_profile = UserProfile.objects.create(user=self.user)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = 'Token ' + self.client.post(path=url,
                                                 data=json_data,
                                                 content_type='application/json').data['access']
        self.user_1 = User.objects.create(username='user_1',
                                          password=password,
                                          is_active=True)
        self.user_profile_1 = UserProfile.objects.create(user=self.user_1,
                                                         is_shop=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = 'Token ' + self.client.post(path=url,
                                                   data=json_data_1,
                                                   content_type='application/json').data['access']

        self.user_2 = User.objects.create(username='user_2',
                                          password=password,
                                          is_active=True)
        self.user_profile_2 = UserProfile.objects.create(user=self.user_2)
        data_2 = {
            'username': self.user_2.username,
            'password': 'password'
        }
        json_data_2 = json.dumps(data_2)
        self.token_2 = 'Token ' + self.client.post(path=url,
                                                   data=json_data_2,
                                                   content_type='application/json').data['access']

        self.category = Category.objects.create(name='category')
        self.category_1 = Category.objects.create(name='category_1')

        self.product = Product.objects.create(name='product',
                                              price='22.00',
                                              discount='10.00',
                                              material='material',
                                              service_life=2,
                                              guarantee=1,
                                              description='description',
                                              user=self.user,
                                              category=self.category)
        self.product_1 = Product.objects.create(name='product_1',
                                                price='10.00',
                                                material='material_1',
                                                description='description_1',
                                                user=self.user_1,
                                                category=self.category_1)

    def test_get(self):
        """Тест для получения списка продуктов"""

        url = reverse('product-list')
        products = Product.objects.all().annotate(
            price_with_discount=F('price') - F('discount')
        )
        data = ProductModelSerializer(products, many=True).data
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)

    def test_create_is_shop(self):
        """Тест для создания продукта магазином"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'name': 'create_product',
            'price': '130.00',
            'material': 'create_material',
            'description': 'create_description',
            'user': self.user_1.id,
            'category': self.category_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Product.objects.all().count())

    def test_create_not_shop_but_staff(self):
        """Тест для создания продукта не магазином а администратором"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'name': 'create_product',
            'price': '130.00',
            'material': 'create_material',
            'description': 'create_description',
            'user': self.user_1.id,
            'category': self.category_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Product.objects.all().count())

    def test_create_not_shop(self):
        """Тест для создания продукта не магазином а администратором"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'name': 'create_product',
            'price': '130.00',
            'material': 'create_material',
            'description': 'create_description',
            'user': self.user_1.id,
            'category': self.category_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Product.objects.all().count())

    def test_update_owner(self):
        """Тест для обновления полей продукта владельцем"""

        self.assertEqual(self.category_1.id, self.product_1.category.id)
        self.assertEqual(0.00, self.product_1.discount)
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {
            'name': 'product_1',
            'price': '10.00',
            'material': 'material_1',
            'description': 'description_1',
            'user': self.user_1.id,
            'category': self.category.id,
            'discount': '5.00'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(5.00, self.product_1.discount)
        self.assertEqual(self.category.id, self.product_1.category.id)

    def test_update_not_owner_but_staff(self):
        """Тест для обновления полей продукта не владельцем а администратором"""

        self.assertEqual(self.category_1.id, self.product_1.category.id)
        self.assertEqual(0.00, self.product_1.discount)
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {
            'name': 'product_1',
            'price': '10.00',
            'material': 'material_1',
            'description': 'description_1',
            'user': self.user_1.id,
            'category': self.category.id,
            'discount': '5.00'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(5.00, self.product_1.discount)
        self.assertEqual(self.category.id, self.product_1.category.id)

    def test_update_not_owner(self):
        """Тест для обновления полей продукта не владельцем"""

        url = reverse('product-detail', args=(self.product_1.id,))
        data = {
            'name': 'product_1',
            'price': '10.00',
            'material': 'material_1',
            'description': 'description_1',
            'user': self.user_1.id,
            'category': self.category.id,
            'discount': '5.00'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_owner(self):
        """Тест для удаления продукта владельцем"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Product.objects.all().count())

    def test_delete_not_owner_but_staff(self):
        """Тест для удаления продукта не владельцем а администратором"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Product.objects.all().count())

    def test_delete_not_owner(self):
        """Тест для удаления продукта не владельцем а администратором"""

        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Product.objects.all().count())
