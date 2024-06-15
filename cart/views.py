from django.shortcuts import render
# from .models import Cart

# Create your views here.
def view_cart(request):
        """
        A view that renders the bag contents page
        """
        
        return render(request, 'cart/cart.html', context)
