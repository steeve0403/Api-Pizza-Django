from django.db import models
from PIL import Image as PILImage

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.description or f"Image {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = PILImage.open(self.image.path)
        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except Exception as e:
            print(f"Error deleting image file: {e}")
        super().delete(*args, **kwargs)

    def create_thumbnail(self):
        img = PILImage.open(self.image.path)
        img.thumbnail((200, 200))
        thumbnail_path = self.image.path.replace('images/', 'thumbnails/')
        img.save(thumbnail_path)
        return thumbnail_path

    @staticmethod
    def cleanup_orphaned_images():
        for image in Image.objects.all():
            if not image.custom_pizzas.exists() and not image.ingredients.exists():
                image.delete()

    class Meta:
        indexes = [
            models.Index(fields=['description']),
            models.Index(fields=['is_default']),
        ]
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
