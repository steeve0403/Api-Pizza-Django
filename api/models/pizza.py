from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

from api.models.category import Category
from api.models.image import Image
from api.models.ingredients import Ingredient


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='pizzas', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='pizzas')
    custom_images = models.ManyToManyField(Image, related_name='custom_pizzas', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.ingredients.count() < 3:
            raise ValidationError("A pizza must have at least 3 ingredients.")
        if not self.price:
            raise ValidationError("A pizza must have a price.")

    def get_image(self):
        if self.custom_images.exists():
            return self.custom_images.first()
        return Image.objects.get(id=1)

    def get_absolute_url(self):
        return reverse('pizza_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Pizza'
        verbose_name_plural = 'Pizzas'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]
