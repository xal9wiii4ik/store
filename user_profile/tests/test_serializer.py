from django.contrib.auth.models import User
from django.db.models import F
from django.test import TestCase

from user_profile.models import UserProfile
from user_profile.serializer import UserProfileModelSerializer


class UserProfileTestCase(TestCase):
    """Test for userprofile serializer"""

    def test_ok(self):
        """Validation data of userprofile"""

        self.user = User.objects.create(username='user',
                                        email='email@mail.ru',
                                        first_name='first_name',
                                        last_name='last_name')
        self.user_1 = User.objects.create(username='user_1',
                                          email='email_1@mail.ru',
                                          first_name='first_name_1',
                                          last_name='last_name_1')
        self.userprofile = UserProfile.objects.create(user=self.user,
                                                      phone='phone')
        self.userprofile_1 = UserProfile.objects.create(user=self.user_1,
                                                        phone='phone_1',
                                                        is_shop=True)

        user_profiles = UserProfile.objects.all().annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            email=F('user__email'),
            username=F('user__username'),
        )
        data = UserProfileModelSerializer(user_profiles, many=True).data
        expected_data = [
            {
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'phone': 'phone',
                'address': '',
                'is_shop': False,
                'date_joined': data[0]['date_joined'],
                'updated_on': data[0]['updated_on'],
                'legal_address': '',
                'unp': '',
                'bank_detail': '',
            },
            {
                'username': self.user_1.username,
                'first_name': self.user_1.first_name,
                'last_name': self.user_1.last_name,
                'email': self.user_1.email,
                'phone': 'phone_1',
                'address': '',
                'is_shop': True,
                'date_joined': data[1]['date_joined'],
                'updated_on': data[1]['updated_on'],
                'legal_address': '',
                'unp': '',
                'bank_detail': '',
            }
        ]
        self.assertEqual(expected_data, data)
