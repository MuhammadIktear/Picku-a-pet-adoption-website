# Generated by Django 5.0.6 on 2024-08-11 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0018_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='picku/pet_image'),
        ),
    ]
