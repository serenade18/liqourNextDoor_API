from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission

from liquornextdoorApp.models import UserAccount


@receiver(post_save, sender=UserAccount)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_bar:
            permissions = Permission.objects.filter(codename__startswith='bar_')
            instance.user_permissions.add(*permissions)
        elif instance.is_liquor_store:
            permissions = Permission.objects.filter(codename__startswith='liquor_')
            instance.user_permissions.add(*permissions)
