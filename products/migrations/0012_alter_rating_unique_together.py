# Generated by Django 5.0.6 on 2024-07-06 16:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_rating_rating_alter_rating_product_alter_rating_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('product', 'user')},
        ),
    ]
