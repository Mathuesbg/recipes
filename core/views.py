from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/pages/home.html', context={"name": "matheus"})

def recipe(request, id):
        return render(request, 'core/pages/recipe-view.html', context={"name": "matheus"})
