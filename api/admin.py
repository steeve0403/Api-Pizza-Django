from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Pizza, Ingredient


# Register your models here.

class IngredientInLine(admin.TabularInline):
    model = Pizza.ingredients.through
    extra = 1
    can_delete = True


class ImageInline(admin.TabularInline):
    model = Pizza.custom_images.through
    extra = 1


# @admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'vegetarian', 'available')
    search_fields = ['name', 'description', 'price', 'vegetarian', 'available']
    inlines = [ImageInline, IngredientInLine]

    def default_image(self, obj):
        if obj.default_image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                               obj.default_image.image.url)
        return None

    default_image.short_description = 'Default Image'


# @admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ['name']


# @admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'description']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)

    image_tag.short_description = 'Image'


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Image, ImageAdmin)
