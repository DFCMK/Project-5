# Generated by Django 5.0.6 on 2024-06-25 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_user_wishlist_product_users_wishlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='product_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
