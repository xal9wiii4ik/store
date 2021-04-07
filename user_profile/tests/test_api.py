import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import F
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from user_profile.models import UserProfile
from user_profile.serializer import UserProfileModelSerializer


class UserProfileApiTestCase(APITestCase):
    """Test user profile"""

    def setUp(self):
        url = reverse('auth_path:token')
        password = make_password('password')
        self.user = User.objects.create(username='user',
                                        email='email@mail.ru',
                                        first_name='first_name',
                                        last_name='last_name',
                                        password=password,
                                        is_active=True,
                                        is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = 'Token ' + self.client.post(url, data=json_data,
                                                 content_type='application/json').data['access']

        self.user_1 = User.objects.create(username='user_1',
                                          email='email_1@mail.ru',
                                          first_name='first_name_1',
                                          last_name='last_name_1',
                                          password=password,
                                          is_active=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = 'Token ' + self.client.post(url, data=json_data_1,
                                                   content_type='application/json').data['access']

        self.user_2 = User.objects.create(username='user_2',
                                          email='email@mail.ru',
                                          first_name='first_name',
                                          last_name='last_name',
                                          password=password,
                                          is_active=True)
        data_2 = {
            'username': self.user_2.username,
            'password': 'password'
        }
        json_data_2 = json.dumps(data_2)
        self.token_2 = 'Token ' + self.client.post(url, data=json_data_2,
                                                   content_type='application/json').data['access']

        self.userprofile = UserProfile.objects.create(user=self.user,
                                                      phone='phone')
        self.userprofile_1 = UserProfile.objects.create(user=self.user_1,
                                                        phone='phone_1',
                                                        is_shop=True)

    def test_get_staff(self):
        """Get user profiles (admin token)"""

        url = reverse('userprofile-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        user_profiles = UserProfile.objects.all().annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email'),
            username=F('user__username'),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(UserProfileModelSerializer(user_profiles, many=True).data,
                         response.data)

    def test_get_not_staff(self):
        """Get user profiles (user token)"""

        url = reverse('userprofile-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_impossible_create_staff(self):
        """Create user profiles (haven`t permission)"""

        self.assertEqual(2, UserProfile.objects.all().count())
        url = reverse('userprofile-list')
        user_create_1 = User.objects.create(username='user_create')
        data = {
            'user': user_create_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        try:
            self.client.post(path=url, data=json_data,
                             content_type='application/json')
        except IntegrityError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_delete_owner(self):
        """Delete profile (user token)"""

        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_not_owner(self):
        """Delete profile (different user token)"""

        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_not_owner_but_staff(self):
        """Delete profile (admin token)"""

        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_update_owner(self):
        """Update profile (user token)"""

        self.assertEqual('phone_1', UserProfile.objects.get(id=self.userprofile_1.id).phone)
        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        data = {
            'phone': 'Iphone'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.userprofile_1.refresh_from_db()
        self.assertEqual('Iphone', UserProfile.objects.get(id=self.userprofile_1.id).phone)

    def test_update_not_owner(self):
        """Update profile (different user token)"""

        self.assertEqual('phone_1', UserProfile.objects.get(id=self.userprofile_1.id).phone)
        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        data = {
            'phone': 'Iphone'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_not_owner_but_staff(self):
        """Update profile (admin token)"""

        self.assertEqual('phone_1', UserProfile.objects.get(id=self.userprofile_1.id).phone)
        url = reverse('userprofile-detail', args=(self.userprofile_1.id,))
        data = {
            'phone': 'Iphone'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.userprofile_1.refresh_from_db()
        self.assertEqual('Iphone', UserProfile.objects.get(id=self.userprofile_1.id).phone)
