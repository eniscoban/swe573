# Generated by Django 3.0.5 on 2020-05-10 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200506_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_photo',
            field=models.CharField(default='prf_2.png', max_length=30),
        ),
    ]
