from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html', context={"name": "matheus"})

def base(request):
    return render(request, 'global/home.html')