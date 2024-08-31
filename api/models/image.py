from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or f"Image {self.id}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

@receiver(post_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    instance.image.delete()
