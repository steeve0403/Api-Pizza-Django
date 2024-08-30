from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Pizza

@receiver(post_save, sender=Pizza)
def update_last_modified(sender, instance, **kwargs):
    instance.last_modified = timezone.now()
    instance.save()

@receiver(post_delete, sender=Pizza)
def delete_custom_images(sender, instance, **kwargs):
    instance.custom_images.clear()