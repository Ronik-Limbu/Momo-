# Generated by Django 5.1.3 on 2024-11-26 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='created_at',
        ),
    ]
