# Generated by Django 5.0.6 on 2024-08-11 06:51

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='picku/profile_image'),
        ),
    ]
