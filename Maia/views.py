from django.shortcuts import render
from django.http import Http404

# Create your views here.
def dashboard(request):
    return render(request, 'base.html')