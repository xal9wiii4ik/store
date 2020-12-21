from django.contrib import admin

from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone',
                    'address', 'is_shop',
                    'legal_address', 'unp', 'bank_detail')
