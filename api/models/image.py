from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or f"Image {self.id}"
