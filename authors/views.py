from django.shortcuts import render, redirect
from authors.forms import RegisterForm
from django.http import Http404
from django.contrib import messages

def register_author(request):
    
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register.html', {'form': form})


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