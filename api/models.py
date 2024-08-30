from django.db import models


# Create your models here.

class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or f"Images {self.id}"


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField('Ingredient', related_name='pizzas')
    default_image = models.ForeignKey(Images, on_delete=models.SET_NULL, null=True,
                                      related_name='default_pizzas')
    custom_images = models.ManyToManyField(Images, related_name='custom_pizzas',
                                           blank=True)
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='some default description')
    images = models.ManyToManyField(Images, related_name='ingredients',
                                    blank=True)  # Lien vers les images des ingrédients
    def __str__(self):
        return self.name
