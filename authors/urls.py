from django.urls import path
from authors import views


app_name = 'authors'
urlpatterns = [
    path('register/', views.register_author, name='register'),
    path('register/create/', views.register_create, name='register_create'),

    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),

    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashborad, name='dashboard'),
    
    path(
        "dashboard/recipe/create", 
        views.dashborad_recipe_create, 
        name="dashboard_recipe_create"
        ),

    path(
        'dashboard/recipe/<int:id>/edit/', 
        views.dashborad_recipe_edit, 
        name='dashboard_recipe_edit'
        ),    
     

]