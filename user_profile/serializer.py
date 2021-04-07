from rest_framework import serializers

from user_profile.models import UserProfile


class UserProfileModelSerializer(serializers.ModelSerializer):
    """Serializer for User profile"""

    first_name = serializers.CharField(max_length=60, read_only=True)
    last_name = serializers.CharField(max_length=60, read_only=True)
    email = serializers.CharField(max_length=60, read_only=True)
    username = serializers.CharField(max_length=60, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'address',
                  'is_shop', 'date_joined', 'updated_on',
                  'legal_address', 'unp', 'bank_detail']
        read_only_fields = ['is_shop']
