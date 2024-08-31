from django.db import models
from django.core.exceptions import ValidationError

from api.models.image import Image


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


    class Meta:
        verbose_name = 'Ingredient'
    verbose_name_plural = 'Ingredients'