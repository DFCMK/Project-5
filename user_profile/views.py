from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Wishlist, Address
from products.models import Product
from .forms import UserProfileForm, AddressForm

from checkout.models import Order

@login_required
def profile(request):
    """ 
    Display the user's profile.
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist = Wishlist.objects.filter(user=user)
    orders = profile.orders.all()
    address = Address.objects.filter(user=user)
    default_address = Address.objects.filter(user=request.user, set_as_default=True).first()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    template = 'user_profile/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'wishlist': wishlist,
        'address': address,
        'default_address': default_address,
        'on_profile_page': True,
    }

    return render(request, template, context)

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

# Based on Very Academys tutorial:
# https://www.youtube.com/watch?v=OgA0TTKAtqQ
@login_required
def add_to_wishlist(request, id):
    '''
    Save Products to a Whishlist, for later purchase
    '''
    product = get_object_or_404(Product, id=id)
    wishlist_entry, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    wishlist_count = request.user.wishlist_entries.count()
    if created:
        messages.success(request, f'{product.name} was successfully added to your Wishlist!')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    else: 
        messages.error(request, f'{product.name} is already in your wishlist!')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def wishlist(request):
    '''
    Filter for products in wishlist and assosite them with the user
    '''
    
    wishlist_entries = Wishlist.objects.filter(user=request.user)
    products = [entry.product for entry in wishlist_entries]
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        "wishlist": products,
        "wishlist_count": wishlist_count
    }

    return render(request, "user_profile/wishlist.html", context)

@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    wishlist_entry = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_entry:
        wishlist_entry.delete()
        messages.success(request, f'{product.name} deleted from Wishlist!')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    else:
        messages.error(request, 'Wishlist entry not found!')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def add_address(request):
    user_profile = request.user.userprofile
    default_address = Address.objects.filter(user=request.user, set_as_default=True).first()

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user

            # If a new address is set as default
            if address_form.cleaned_data.get('set_as_default', False):
                # Unset the previous default address if it exists
                if default_address:
                    default_address.set_as_default = False
                    default_address.save()
                
                address.set_as_default = True
                # Update the user profile default address fields
                user_profile.default_full_name = address.full_name
                user_profile.default_phone_number = address.phone_number
                user_profile.default_country = address.country
                user_profile.default_postcode = address.postcode
                user_profile.default_town_or_city = address.town_or_city
                user_profile.default_street_address1 = address.street_address1
                user_profile.default_street_address2 = address.street_address2
                user_profile.default_county = address.county
                user_profile.save()
            address.save()
            messages.success(request, 'Address added successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error adding address. Please check the form.')
    else:
        address_form = AddressForm()

    context = {
        'address_form': address_form,
        'default_address': default_address
    }

    return render(request, 'user_profile/add_address.html', context)
