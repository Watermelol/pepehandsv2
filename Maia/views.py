from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import user_profile
from .forms import UserProfile

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        # check if the user got answer the questionair before or not
        current_user = user_profile.objects.get(user_id=request.user.id)
        questionaire_answered = getattr(current_user, 'questionaire_answered')
        # if user answer b4 then redirect him to dashboard else bring him to questionaire page
        if (questionaire_answered == True):
            return render(request, 'dashboard.html')
        else:
            return redirect('/questionaire/user-profile')
    

def login(request):
    # check if the user is log in ady or not
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'login.html')

def logout_account(request):
    logout(request)
    return render(request, 'login.html')

def to_questionaire_user_profile(request):
    user_form = UserProfile()
    context = {'user_form': user_form}
    return render(request, 'questionaire_user_profile.html', context)