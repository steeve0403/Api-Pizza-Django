from django.contrib import admin
from .models import Pizza, Ingredient
# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'vegetarian', 'available')
    search_fileds = ['name', 'description', 'price', 'vegetarian', 'available']

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fileds = ['name', 'description']


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Ingredient, IngredientAdmin)