# Generated by Django 3.0.5 on 2020-05-06 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_recipe_recipe_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='calories_total',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='cautions',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='healthLabels',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='weight_total',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='yield_total',
        ),
        migrations.RemoveField(
            model_name='nutrients',
            name='ingredient_id',
        ),
    ]