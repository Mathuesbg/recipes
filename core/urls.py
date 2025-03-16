from django.urls import path
from core import views

app_name = "recipe"

urlpatterns = [
    
    path('', views.home, name='home'),
    path('recipe/search/', views.search, name='search'),
    path('recipe/category/<int:category_id>/', views.category, name='category'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    ]
