from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_path.serializers import (
    RegistrationSerializer,
    LogInSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from auth_path.services_view import (
    create_user_and_send_email_for_activation,
    activate_user_and_create_user_profile,
    get_tokens, send_mail_to_reset_password,
    _verification_uid_and_token,
    reset_password,
    get_user_profile_id,
)


class RegistrationView(APIView):
    """APIView для регистрации пользователя"""

    def post(self, request):
        if request.data['password'] == request.data['repeat_password']:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                create_user_and_send_email_for_activation(data=serializer.data, request=request)
                return Response(data={'ok': 'Check your mail'},
                                status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'Password is not equal repeat password'},
                        status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    """View для активации пользователя и
    создания """

    def get(self, request, uid, token):
        if activate_user_and_create_user_profile(uid=uid, token=token):
            return Response(data={'ok': 'User has been activate'},
                            status=status.HTTP_200_OK)
        return Response(data={'error': 'Un valid uid or token'},
                        status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    """View для авторизации пользователя и выдачи токена"""

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            data = get_tokens(data=serializer.data, request=request)
            data.update(
                {
                    'id': get_user_profile_id(serializer.data['username'])
                }
            )
            return Response(data=data,
                            status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """View для сброса пароля"""

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            send_mail_to_reset_password(data=serializer.data, request=request)
            return Response(data={'ok': 'Message has been send to your email'},
                            status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """View для сброса и установки нового пароля"""

    def get(self, request, uid, token):
        if _verification_uid_and_token(uid=uid, token=token):
            return Response(data={'uid': uid, 'token': token},
                            status=status.HTTP_200_OK)
        return Response(data={'error': 'Un valid uid or token'},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if request.data['password'] == request.data['repeat_password']:
                reset_password(uid=uid, token=token, data=serializer.data)
                return Response(data={'ok': 'Password has been changed'},
                                status=status.HTTP_200_OK)
        return Response(data={'uid': uid, 'token': token},
                        status=status.HTTP_400_BAD_REQUEST)


class VerificationPermissionOfUserView(APIView):
    """Проверка прав пользователя"""

    def post(self, request):
        if request.user.is_staff:
            return Response(data={'ok': 'Your token is valid'}, status=status.HTTP_200_OK)
        return Response(data={'error': 'You are not the staff'}, status=status.HTTP_403_FORBIDDEN)
