"""
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from liquornextdoorApp.views import UserViewSet, AdminUserViewSet, UserInfoView, BarUserViewSet, LiquorStoreUserViewSet, \
    LocationViewSet
from liquornextdoorProject import settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')
router.register(r'bars/users', BarUserViewSet, basename='bar-user')
router.register(r'liquor/users', LiquorStoreUserViewSet, basename='liquor-store-user')
router.register(r'location', LocationViewSet, basename='location')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/verify/', UserViewSet.as_view({'post': 'verify_otp'}), name='verify-user'),
    path('api/admin/verify/', AdminUserViewSet.as_view({'post': 'verify_otp'}), name='admin-verify'),
    path('api/bars/verify/', BarUserViewSet.as_view({'post': 'verify_otp'}), name='verify-bars'),
    path('api/liquor/verify/', LiquorStoreUserViewSet.as_view({'post': 'verify_otp'}), name='verify-liquorstore'),
    path('api/userinfo/', UserInfoView.as_view(), name='userinfo'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
