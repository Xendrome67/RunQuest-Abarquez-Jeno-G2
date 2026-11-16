from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    Signal to handle actions when a new user is created.
    Currently a placeholder for future extensions (e.g., sending welcome email).
    """
    if created:
        # Could send welcome email here
        pass