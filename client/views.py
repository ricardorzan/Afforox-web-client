from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import View


def Homepage(request):
    return render(request, "home.html")

def About(request):
    return render(request, "about.html")