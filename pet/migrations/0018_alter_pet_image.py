# Generated by Django 5.0.6 on 2024-08-11 07:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0017_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='pet_image'),
        ),
    ]
