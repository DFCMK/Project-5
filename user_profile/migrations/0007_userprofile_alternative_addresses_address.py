# Generated by Django 5.0.6 on 2024-06-28 10:11

import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_alter_wishlist_user_alter_wishlist_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alternative_addresses',
            field=models.ManyToManyField(blank=True, to='user_profile.userprofile'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_full_name', models.CharField(default='', max_length=50)),
                ('default_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('default_street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('default_street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('default_town_or_city', models.CharField(blank=True, max_length=40, null=True)),
                ('default_county', models.CharField(blank=True, max_length=80, null=True)),
                ('default_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('default_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
