"""
URL configuration for liquornextdoorProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from liquornextdoorApp.views import UserViewSet, AdminUserViewSet, UserInfoView, BarUserViewSet, LiquorStoreUserViewSet
from liquornextdoorProject import settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')
router.register(r'bars/users', BarUserViewSet, basename='bar-user')
router.register(r'liquor/users', LiquorStoreUserViewSet, basename='liquor-store-user')

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
