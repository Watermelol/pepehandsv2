from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import logout

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')

def logout_account(request):
    logout(request)
    return render(request, 'login.html')

def to_questionaire(request):
    return render(request, 'questionaire.html')