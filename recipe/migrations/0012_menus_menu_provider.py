# Generated by Django 3.0.5 on 2020-06-16 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodproviders', '0004_followerprovider'),
        ('recipe', '0011_menu_recipe_menus'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='menu_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodproviders.FoodProviders'),
        ),
    ]
