# Generated by Django 5.0.6 on 2024-07-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_rating_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]