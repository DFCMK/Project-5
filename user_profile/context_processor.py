from products.models import Product


def wishlist_count(request):
    if request.user.is_authenticated:
        count = Product.objects.filter(users_wishlist=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}
