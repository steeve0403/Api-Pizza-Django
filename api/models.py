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
    TYPE_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('meat', 'Meat'),
        ('dairy', 'Dairy'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(default='some default description')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='other')
    allergens = models.TextField(blank=True)
    images = models.ManyToManyField(Image, related_name='ingredients', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.type == 'meat' and self.name.lower() in ['ham', 'bacon']:
            raise ValidationError('This ingredient cannot be added to vegetarian pizzas.')


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
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]
