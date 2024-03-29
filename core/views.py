# core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request, 'core/login.html')

@login_required
def home(request):
    return render(request, 'core/home.html')
