# Generated by Django 5.0.6 on 2024-06-23 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_rename_user_whishlist_product_user_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user_wishlist',
            new_name='users_wishlist',
        ),
    ]
