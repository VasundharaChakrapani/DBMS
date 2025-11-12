from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Equipment Management System is working!")

# Create your views here.
