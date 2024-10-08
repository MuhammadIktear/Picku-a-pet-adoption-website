# Generated by Django 5.0.6 on 2024-07-27 08:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='adopt',
            name='address',
            field=models.CharField(default='Dhaka', max_length=255),
        ),
        migrations.AddField(
            model_name='adopt',
            name='email',
            field=models.CharField(default='a@gmail.com', max_length=50),
        ),
        migrations.AddField(
            model_name='adopt',
            name='full_name',
            field=models.CharField(default='Unknown', max_length=40),
        ),
        migrations.AddField(
            model_name='adopt',
            name='phone_no',
            field=models.CharField(default='01873381172', max_length=12),
        ),
        migrations.AddField(
            model_name='pet',
            name='adopted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adopted_pets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='breed',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_pets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sex',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='pet.pet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
