from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser = apps.get_model('accounts', 'CustomUser')
        if isinstance(instance, CustomUser):
            UserProfile.objects.create(user=instance)