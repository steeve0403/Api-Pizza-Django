from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from django.utils import timezone

from .models.pizza import Pizza


@receiver(post_save, sender=Pizza)
def update_last_modified(sender, instance, **kwargs):
    instance.last_modified = timezone.now()
    instance.save()


@receiver(post_delete, sender=Pizza)
def delete_custom_images(sender, instance, **kwargs):
    instance.custom_images.clear()


@receiver(post_migrate)
def preload_data(sender, **kwargs):
    from .models.category import Category
    if not Category.objects.exists():
        Category.objects.create(name="Standard")
        print("Standard category created.")
