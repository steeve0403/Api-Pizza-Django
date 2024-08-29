from django.db import models

# Create your models here.


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField('Ingredient', related_name='pizzas')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name