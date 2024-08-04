# Generated by Django 5.0.6 on 2024-08-04 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0011_alter_review_author_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='breed',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='color',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='size',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='species',
        ),
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.status'),
        ),
        migrations.AddField(
            model_name='pet',
            name='breed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.breed'),
        ),
        migrations.AddField(
            model_name='pet',
            name='color',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.color'),
        ),
        migrations.AddField(
            model_name='pet',
            name='sex',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.sex'),
        ),
        migrations.AddField(
            model_name='pet',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.size'),
        ),
        migrations.AddField(
            model_name='pet',
            name='species',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pet.species'),
        ),
    ]
