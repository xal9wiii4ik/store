from django.db.models import F

from rest_framework.viewsets import ModelViewSet

from user_profile.models import UserProfile
from user_profile.permissions import IsStaffOrOwnerOnly
from user_profile.serializer import UserProfileModelSerializer


class UserProfileViewSet(ModelViewSet):
    """View for user profile"""

    queryset = UserProfile.objects.all().annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email'),
        username=F('user__username')
    )
    serializer_class = UserProfileModelSerializer
    permission_classes = (IsStaffOrOwnerOnly,)
