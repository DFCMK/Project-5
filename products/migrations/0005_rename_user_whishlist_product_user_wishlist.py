# Generated by Django 5.0.6 on 2024-06-23 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_user_whishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user_whishlist',
            new_name='user_wishlist',
        ),
    ]
