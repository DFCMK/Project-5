from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=50, null=False, blank=False, default='')
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    else: 
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)

#class Address(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    default_full_name = models.CharField(max_length=50, null=False, blank=False, default='')
#    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
#    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
#    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
#    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
#    default_county = models.CharField(max_length=80, null=True, blank=True)
#    default_postcode = models.CharField(max_length=20, null=True, blank=True)
#    default_country = CountryField(blank_label='Country', null=True, blank=True)
#
#    def __str__(self):
#        return f'{self.default_full_name}, {self.default_town_or_city}'

class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist_entries'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='wishlist'
    )

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    class Meta:
        unique_together = ('user', 'product')