from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    users_wishlist = models.ManyToManyField(
        User, related_name='product_wishlist', blank=True)
    total_votes = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.average_rating = round(avg_rating, 1) if \
                avg_rating is not None else None
            self.save()

    def __str__(self):
        return self.name


# Inspired by Denisse Abreu Blog:
# https://codingpr.com/star-rating-blog/
class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars')])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating for {self.product.name} by {self.user.username}"

    class Meta:
        unique_together = ('product', 'user')
