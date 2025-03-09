from django.shortcuts import render, get_list_or_404, get_object_or_404
from core import models

# Create your views here.
def home(request):
    recipes = models.Recipe.objects.filter(is_published=True).order_by("-id")
    return render(
            request=request, 
            template_name='core/pages/home.html', 
            context={
            "recipes": recipes,
            }
        )

def recipe(request, id):
        recipe = get_object_or_404(
            models.Recipe.objects.filter(
                pk=id, 
                is_published=True
                )
            )

        return render(
             
            request=request,
            template_name='core/pages/recipe-view.html',
            context={
                "recipe": recipe,
                "is_detail_page" : True
                }
            )


def category(request, category_id):
    recipes = get_list_or_404(
        models.Recipe.objects.filter(
            category__id = category_id, 
            is_published=True,
        ).order_by("-id")
    )
    
    return render(  
            request=request, 
            template_name='core/pages/category.html', 
            context={
            "recipes": recipes,
            "title": f"{recipes[0]} - Category",
            }
        )