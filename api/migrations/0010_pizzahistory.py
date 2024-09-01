# Generated by Django 5.1 on 2024-09-01 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_allergen_alter_image_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('vegetarian', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pizza')),
            ],
        ),
    ]
