from django.shortcuts import render


def register_author(request):
    return render(request, 'authors/pages/register.html')