from django.shortcuts import render, redirect
from django.urls import reverse
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages

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
    return render(
        request=request,
        template_name= "authors/pages/login.html",
    )