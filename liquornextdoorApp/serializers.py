from rest_framework import serializers
from django.contrib.auth import get_user_model

from liquornextdoorApp.models import UserLocation

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='normal', required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'user_type', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        user_type = attrs.get('user_type', 'normal')
        if user_type not in ['normal', 'admin', 'bars', 'liquor_store']:
            raise serializers.ValidationError("Invalid user type")
        return attrs


class CustomUserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'user_type', 'last_login']


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'user_type', 'is_active', 'is_staff', 'is_admin', 'is_bar', 'is_liquor_store', 'date_joined']


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['id', 'user', 'latitude', 'longitude', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']