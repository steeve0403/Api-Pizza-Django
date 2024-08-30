from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from django.urls import reverse

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or f"Image {self.id}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='some default description')
    images = models.ManyToManyField(Image, related_name='ingredients', blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='pizzas', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='pizzas')
    default_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='default_pizzas')
    custom_images = models.ManyToManyField(Image, related_name='custom_pizzas', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.ingredients.count() < 3:
            raise ValidationError("A pizza must have at least 3 ingredients.")
        if not self.price:
            raise ValidationError("A pizza must have a price.")


    def get_default_image_url(self):
        if self.default_image:
            return self.default_image.image.url
        elif self.custom_images.exists():
            return self.custom_images.first().image.url
        return None

    def get_absolute_url(self):
        return reverse('pizza_detail', args=[str(self.id)])

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]

