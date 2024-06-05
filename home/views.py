from django.shortcuts import render


def home(request):
    '''
    Return to the Homepage
    '''
    return render(request, 'home/index.html')