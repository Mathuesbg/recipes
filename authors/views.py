from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from authors.forms import RegisterForm, LoginForm
from core.models import Recipe


def register_author(request):
    
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)

    return render(
        request=request, 
        template_name='authors/pages/register.html', 
        context={'form': form, 'form_action':  reverse("authors:register_create") }
    )


def register_create(request):
    
    if not request.POST:
        raise Http404  

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        
        user = form.save()
        messages.success(request, 'Author registered successfully!')
        del(request.session['register_form_data'])
        return redirect("authors:login")

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(
        request=request,
        template_name= "authors/pages/login.html",
        context= {
            "form" : form,
            "form_action" : reverse("authors:login_create")
        }
    )

def login_create(request):
    
    if not request.POST:
        raise Http404  
    
    form = LoginForm(request.POST)
    

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
            )
        
        if authenticated_user is not None:

            login(request=request, user=authenticated_user)

            messages.success(
                request=request, 
                message="User Logged in!"
                )
            
            return redirect(reverse("authors:dashboard"))

        
        messages.error(
            request=request,
            message="invalid credentials"
            )
        return redirect(reverse("authors:dashboard"))
    
    messages.error(
        request=request,
        message="Form error!"
        )
    
    return redirect(reverse("authors:login"))

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request=request, message="invalid logout request")
        return redirect(reverse('authors:login'))
    
    if request.POST.get("username") != request.user.username:
        messages.error(request=request, message="invalid logout user")
        return redirect(reverse('authors:login'))
    
    messages.success(request, "logout successfully!")
    logout(request=request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashborad(request):

    recipes = Recipe.objects.filter(
        is_published = False, 
        author = request.user
        )
    
    return render(
        request=request,
        template_name="authors/pages/dashboard.html",
        context= {
            "recipes": recipes
        }
    )