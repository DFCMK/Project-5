from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Rating
from .forms import RateProductForm
from user_profile.models import Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.functions import Lower

from rest_framework import viewsets

# from .serializers import ProductSerializer
from .models import Product

import json


# Based on Boutique ado view
def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect('products')
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to rate a product!')
            return redirect('login')

        stars = int(request.POST.get('stars', 0))
        if stars < 1 or stars > 5:
            messages.error(request, 'Invalid rating value!')
        else:
            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'stars': stars}
            )
            product.update_average_rating()
            if created:
                messages.success(request, 'Your rating has been submitted.')
            else:
                messages.success(request, 'Your rating has been updated.')
            return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'user_rating': user_rating,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """
    Add a product to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    '''
    Edit a product in the store
    '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'{product.name} was updated Successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, f'Updating {product.name} Failed. Please ensure the form is valid!')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    '''
    delete a product from the store
    '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

#@login_required
#def rate_product(request, product_id):
#    '''
#    rate product with star rating system (1-5 stars)
#    '''
#    if request.method == "POST" and request.POST.get("action") == "stars":
#
#        product = get_object_or_404(Product, product_id)
#        star = request.POST.get("star")
#
#        if star and 1 <= int(star) <= 5:
#            product.total_votes += 1
#            product.total_rating += int(star)
#
#            product.average_rating = product.total_rating / product.total_votes
#
#            product.save()

#    product = get_object_or_404(Product, id=product_id)
#    user = request.user
    
#    if request.method == "POST" and request.POST.get("action") == "stars":
#        star = request.POST.get("star", None)
        
#        if star and 1 <= int(star) <= 5:
#            # Create or update the Rating instance
#            rating, created = Rating.objects.update_or_create(
#                product=product,
#                user=request.user,
#                defaults={'user': request.user, 'rating': int(star)},
#                unique_together=['product', 'user']
#            )
#            
#            # Recalculate the product's average rating
#            product.update_average_rating()
#
#            return JsonResponse({'average_rating': product.average_rating})
#        else:
#            return JsonResponse({'error': 'Invalid star rating'}, status=400)

#    return redirect('product_detail', product_id=product_id)

@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        rating_value = int(request.POST['rating'])
        rating, created = Rating.objects.get_or_create(product=product, user=request.user)
        rating.rating = rating_value
        rating.save()
        product.update_average_rating()
        messages.success(request, 'Your rating was submited Successfully!')
        return redirect('product_detail', product_id=product_id)
    else:
        messages.error(request, 'There where a ERROR! with submiting your rating')
    
    return redirect('product_detail', product_id=product_id)






