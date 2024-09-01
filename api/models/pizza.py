from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

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
    last_modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.pk and self.ingredients.count() < 3:
            raise ValidationError("A pizza must have at least 3 ingredients.")
        if not self.price:
            raise ValidationError("A pizza must have a price.")
        if self.vegetarian:
            for ingredient in self.ingredients.all():
                if ingredient.type == 'meat':
                    raise ValidationError("Vegetarian pizza cannot contain meat ingredients.")

    def get_image(self):
        if self.custom_images.exists():
            return self.custom_images.first()
        return Image.objects.filter(id=1).first()

    def get_absolute_url(self):
        return reverse('pizza_detail', args=[str(self.id)])

    def total_ingredient_cost(self):
        return sum(ingredient.cost for ingredient in self.ingredients.all())

    def delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = 'Pizza'
        verbose_name_plural = 'Pizzas'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['vegetarian']),
            models.Index(fields=['available']),
        ]


@receiver(m2m_changed, sender=Pizza.ingredients.through)
def update_pizza_price(sender, instance, action, **kwargs):
    if action == ['post_add', 'post_remove']:
        instance.price = instance.total_ingredient_cost()
        instance.save()


class PizzaHistory(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now_add=True)
