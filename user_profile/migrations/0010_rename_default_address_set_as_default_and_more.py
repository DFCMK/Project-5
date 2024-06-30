# Generated by Django 5.0.6 on 2024-06-30 15:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0009_alter_address_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='default',
            new_name='set_as_default',
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('user', 'set_as_default')},
        ),
    ]
