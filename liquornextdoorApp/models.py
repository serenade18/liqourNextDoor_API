from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, user_type='normal', **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            name=name,
            phone=phone,
            user_type=user_type,
            is_active=True,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        extra_fields = {
            'is_superuser': True,
            'is_staff': True,
            'is_admin': True,
        }
        return self.create_user(email, name, phone, password, 'admin', **extra_fields)

    def create_bar_user(self, email, name, phone, password=None):
        extra_fields = {
            'is_staff': True,
            'is_bar': True,
        }
        return self.create_user(email, name, phone, password, 'bars', **extra_fields)

    def create_liquor_store_user(self, email, name, phone, password=None):
        extra_fields = {
            'is_staff': True,
            'is_liquor_store': True,
        }
        return self.create_user(email, name, phone, password, 'liquor_store', **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal'),
        ('admin', 'Admin'),
        ('bars', 'Bars'),
        ('liquor_store', 'Liquor Store'),
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_bar = models.BooleanField(default=False)
    is_liquor_store = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        if self.is_admin:
            return True  # Admin has all permissions
        if self.is_bar:
            return perm.startswith('bar_')  # Use a naming convention for permissions
        if self.is_liquor_store:
            return perm.startswith('liquor_')
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.is_admin:
            return True
        if self.is_bar:
            return app_label == 'bars'
        if self.is_liquor_store:
            return app_label == 'liquor_store'
        return super().has_module_perms(app_label)


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)  # OTP valid for 10 minutes


class UserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.email} - ({self.latitude}, {self.longitude})'