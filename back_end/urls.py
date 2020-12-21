from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from back_end import settings
from product.views import (
    CategoryViewSet,
    ProductViewSet,
    DesiredListViewSet
)
from user_profile.views import UserProfileViewSet

router = SimpleRouter()
router.register(r'user-profile', UserProfileViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'desired-list', DesiredListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include(('auth_path.urls', 'auth_path'), namespace='auth_path')),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
