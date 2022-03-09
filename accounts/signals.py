from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """"Creates associated profile when user is created."""
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
