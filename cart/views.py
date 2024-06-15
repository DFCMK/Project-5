from django.shortcuts import render, redirect
# from .models import Cart

# Create your views here.
def view_cart(request):
    '''
    A view that renders the bag contents page
    '''
        
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, item_id):
    '''
    Add a quantity of the specified product to the shopping bag
    '''

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['cart'] = bag
    print(request.session['cart'])
    return redirect(redirect_url)
