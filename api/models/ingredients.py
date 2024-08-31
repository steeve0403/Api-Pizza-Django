from django.db import models
from django.core.exceptions import ValidationError

from api.models.image import Image


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='some default description')

    def __str__(self):
        return self.name


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
    allergens = models.ManyToManyField(Allergen, related_name='ingredients', blank=True)
    images = models.ManyToManyField(Image, related_name='ingredients', blank=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.type == 'meat' and self.name.lower() in ['ham', 'bacon']:
            vegetarians_pizzas = self.pizzas.filter(vegetarian=True)
            if vegetarians_pizzas.exists():
                raise ValidationError('This ingredient cannot be added to vegetarian pizzas.')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
