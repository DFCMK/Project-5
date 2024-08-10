from django.shortcuts import render


def home(request):
    '''
    Return to the Homepage and updated wishlist count
    '''

    if request.user.is_authenticated:
        wishlist_count = request.user.wishlist_entries.count()
    else:
        wishlist_count = 0

    context = {'wishlist_count': wishlist_count}

    return render(request, 'home/index.html', context)
