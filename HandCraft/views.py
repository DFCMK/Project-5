from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def handler404(request, exception):
    '''
    Error Handler 404 - Page not found
    '''
    return render(request, 'errors/404.html', status=404)

def handler403(request, exception):
    '''
    Error Handler 403 - Forbidden
    '''
    return render(request, 'errors/403.html', status=403)

def handler500(request):
    '''
    Error Handler 500 - Internal Server Error
    '''
    return render(request, 'errors/404.html', status=500)

@csrf_exempt
def csp_report(request):
    if request.method == 'POST':
        report = json.loads(request.body)

        print(report)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'method not allowed'}, status=405)
