# Generated by Django 5.0.6 on 2024-08-11 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0021_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
