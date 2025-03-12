from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/category/<int:category_id>/', views.category, name='category'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    path('recipe/search/', views.recipe, name='search'),
    ]
