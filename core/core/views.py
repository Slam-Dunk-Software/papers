from django.shortcuts import render
from django.contrib import messages

def home(request):
    messages.success(request, "Welcome! This is a test message!")
    return render(request, "home.html")
