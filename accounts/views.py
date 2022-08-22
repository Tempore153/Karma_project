from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'accounts/dashboard.html')

def about(request):
    return render(request, 'accounts/about.html')

def donate(request):
    return render(request, 'accounts/donate.html')