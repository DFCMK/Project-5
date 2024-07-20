from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category, Rating
from .forms import RatingForm, ProductForm
from user_profile.models import Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.db.models.functions import Lower

from django.template.loader import render_to_string
from decimal import Decimal

from .models import Product

import json


# Based on Boutique ado view
def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.user.is_authenticated:
        wishlist_count = request.user.wishlist_entries.count()
    else:
        wishlist_count = 0


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
        'wishlist_count': wishlist_count
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Rating.objects.filter(product=product)
    user_rating = None

    if request.user.is_authenticated:
        wishlist_count = request.user.wishlist_entries.count()
    else:
        wishlist_count = 0

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

    # Calculate average rating for display
    avg_rating = product.rating if product.rating else 0
    full_stars = int(avg_rating)
    half_star = 1 if avg_rating % 1 >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    context = {
        'product': product,
        'user_rating': user_rating,
        'wishlist_count': wishlist_count,
        'reviews': reviews,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
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

@login_required
def rate_product(request, product_id):
    '''
    Rate product and leave review
    '''
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            review_text = form.cleaned_data['review']

            try:
                rating = Rating.objects.get(product=product, user=request.user)
            except Rating.DoesNotExist:
                rating = Rating(product=product, user=request.user)

            rating.rating = rating_value
            rating.review = review_text
            rating.save()

            product.update_average_rating()

            reviews = Rating.objects.filter(product=product).order_by('-rating')
            average_rating = calculate_average_rating(reviews)

            reviews_html = render_to_string('products/includes/review_list.html', {'reviews': reviews, 'average_rating': average_rating})
            return JsonResponse({'reviews_html': reviews_html})

        return JsonResponse({'error': 'Form is not valid'}, status=400)

    form = RatingForm()
    reviews = Rating.objects.filter(product=product).order_by('-rating')
    average_rating = calculate_average_rating(reviews)
    return render(request, 'products/rate_product.html', {'product': product, 'reviews': reviews, 'form': form, 'average_rating': average_rating})

def calculate_average_rating(reviews):
    '''
    Calculate average rating out of the total ratings
    '''
    if reviews.exists():
        total_ratings = sum([review.rating for review in reviews])
        average_rating = total_ratings / reviews.count()
        return round(average_rating, 1)
    return 0
    
def edit_review(request, product_id, review_id):
    '''
    Edit given review, with a repopulated form.
    '''
    product = get_object_or_404(Product, pk=product_id)
    
    try:
        review = Rating.objects.get(pk=review_id, product=product, user=request.user)
    except Rating.DoesNotExist:
        return JsonResponse({'error': 'Review does not exist or you do not have permission to edit it.'}, status=404)
    
    if request.method == 'GET':
        # Return review data as JSON
        return JsonResponse({'rating': review.rating, 'review': review.review})
    
    elif request.method == 'POST':
        form = RatingForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            product.update_average_rating()
            
            reviews = Rating.objects.filter(product=product).order_by('-rating')
            max_value = 5 if not reviews.exists() else reviews.first().rating
            reviews_html = render_to_string('products/includes/review_list.html', {'reviews': reviews, 'max_value': max_value})

            return JsonResponse({'reviews_html': reviews_html})
        
        return JsonResponse({'error': 'Form is not valid'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_review(request, product_id, review_id):
    if request.method == 'POST':
        try:
            review = get_object_or_404(Rating, pk=review_id, product_id=product_id, user=request.user)
            review.delete()
            messages.success(request, f'Your review ({review_id}) has been deleted successfully.')
        except Rating.DoesNotExist:
            messages.error(request, 'The review you are trying to delete does not exist.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('product_detail', product_id=product_id)
    else:
        messages.error(request, 'Invalid request method!')
        return redirect(reverse('delete_review', kwargs={'product_id': 'product_id', 'review_id': 'review_id'}))