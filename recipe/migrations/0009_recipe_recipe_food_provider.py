# Generated by Django 3.0.5 on 2020-06-15 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodproviders', '0003_auto_20200615_2027'),
        ('recipe', '0008_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_food_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodproviders.FoodProviders'),
        ),
    ]
