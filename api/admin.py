from django.contrib import admin
from django.utils.html import format_html

from api.models.image import Image
from api.models.ingredients import Ingredient
from api.models.pizza import Pizza


# Register your models here.

class IngredientInLine(admin.TabularInline):
    model = Pizza.ingredients.through
    extra = 1
    can_delete = True


class ImageInline(admin.TabularInline):
    model = Pizza.custom_images.through
    extra = 1
    can_delete = True


@admin.register(Pizza)
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


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    search_fields = ['name', 'type']



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'description']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return None
    image_tag.short_description = 'Preview Image'


# admin.site.register(Pizza)
# admin.site.register(Ingredient)
# admin.site.register(Image)
