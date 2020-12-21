import json

import requests

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from rest_framework.authtoken.models import Token

from auth_path.models import Uid
from back_end import settings
from user_profile.models import UserProfile


def get_user_profile_id(username: str) -> int:
    user = User.objects.get(username=username)
    return UserProfile.objects.get(user=user.id).id


def create_user_and_send_email_for_activation(data: dict, request) -> None:
    """Создание пользователя и отправка
    письма на почту для активации"""

    user = User.objects.create(username=data['username'],
                               password=data['password'],
                               email=data['email'],
                               last_name=data['last_name'],
                               first_name=data['first_name'],
                               is_active=False)
    new_data = _create_unique_uid_and_token(user=user)
    url = _get_web_url(is_secure=request.is_secure(),
                       host=request.get_host(),
                       url=f'/auth/activation/{new_data["uid"]}/{new_data["token"]}')
    send_mail(subject='Activation mail',
              message=f'Your activation link: \n {url}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[data['email']],
              fail_silently=False)


def activate_user_and_create_user_profile(uid: str, token: str) -> bool:
    """Активация пользователя и создание профиля пользователя"""

    if _verification_uid_and_token(uid=uid, token=token):
        verification_data = _get_verification_data_or_404(
            uid=uid,
            token=token
        )
        UserProfile.objects.create(
            user=verification_data['uid_object'].user
        )
        verification_data['uid_object'].user.is_active = True
        verification_data['uid_object'].user.last_login = timezone.now()
        verification_data['uid_object'].user.save()
        _delete_object_or_uid_and_token(uid_object=verification_data['uid_object'],
                                        token_object=verification_data['token_object'])
        return True
    else:
        return False


def send_mail_to_reset_password(data: dict, request) -> None:
    """Отправка письма на почту для сброса пароля"""

    new_data = _create_unique_uid_and_token(
        user=User.objects.get(email=data['email'])
    )
    url = _get_web_url(is_secure=request.is_secure(),
                       host=request.get_host(),
                       url=f'/auth/reset_password/{new_data["uid"]}/{new_data["token"]}')
    send_mail(subject='Reset password',
              message=f'Your link for reset password: \n {url}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[data['email']],
              fail_silently=False)


def reset_password(uid: str, token: str, data: dict) -> None:
    """Сброс пароля"""

    verification_data = _get_verification_data_or_404(
        uid=uid,
        token=token
    )

    verification_data['token_object'].user.password = data['password']
    verification_data['token_object'].user.save()
    _delete_object_or_uid_and_token(uid_object=verification_data['uid_object'],
                                    token_object=verification_data['token_object'])


def get_tokens(data: dict, request) -> dict:
    """Получение токенов"""

    url = _get_web_url(
        is_secure=request.is_secure(),
        host=request.get_host(),
        url=reverse('auth_path:token')
    )
    response = requests.post(url=url,
                             json=data)
    data = {
        'refresh': response.json()['refresh'],
        'access': response.json()['access']
    }
    return data


def _delete_object_or_uid_and_token(uid_object, token_object) -> None:
    """Удаление объектов юида и токена"""

    uid_object.delete()
    token_object.delete()


def _get_verification_data_or_404(uid: str, token: str) -> dict:
    """Получение объектов юида и токена"""

    uid_object = get_object_or_404(klass=Uid,
                                   uid=uid)
    token_object = get_object_or_404(klass=Token,
                                     key=token)
    return {
        'uid_object': uid_object,
        'token_object': token_object
    }


def _get_web_url(is_secure: bool, host: str, url: str) -> str:
    """Получение ссылки"""

    protocol = 'https://' if is_secure else 'http://'
    web_url = protocol + host
    return web_url + url


def _create_unique_uid_and_token(user) -> dict:
    """Создание уникального юида и токена
    для потдверждения уникальности пользователя"""

    uid = Uid.objects.create(user=user)
    token = Token.objects.create(user=user)
    return {
        'uid': uid.uid,
        'token': token.key
    }


def _verification_uid_and_token(uid: str, token: str) -> bool:
    """Проверка юида и токена на правильность"""

    verification_data = _get_verification_data_or_404(
        uid=uid,
        token=token
    )

    if verification_data['token_object'].user == verification_data['uid_object'].user:
        return True
    return False
