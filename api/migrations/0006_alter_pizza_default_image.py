# Generated by Django 5.1 on 2024-08-30 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_category_ingredient_allergens_ingredient_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='default_image',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_pizzas', to='api.image'),
        ),
    ]
