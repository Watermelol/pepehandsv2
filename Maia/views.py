from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import user_profile
from .forms import UserProfile
from djstripe.models import Charge
import json
import stripe

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        current_user = user_profile.objects.get(user_id=request.user.id)
        user_agreement = getattr(current_user, 'user_agreement')
        #Check if user agreeded the agreement ady or not
        if (user_agreement != True):
            return redirect('/end-user-agreement')
        elif (user_agreement == True):
            user_profile_updated = getattr(current_user, 'user_profile_updated')
            financial_data_provided = getattr(current_user, 'financial_data_provided')
            qualitative_data_provided = getattr(current_user, 'qualitative_data_provided')
            # check if the user got answer the questionair before or not
            if (user_profile_updated != True):
                return redirect('/questionaire/user-profile')
            elif (financial_data_provided != True):
                return redirect('/financial_data_questionaire')
            # if user answer b4 then redirect him to dashboard else bring him to questionaire page
            else:
                return render(request, 'dashboard.html')

# Login Logout
def login(request):
    # check if the user is log in ady or not
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render(request, 'login.html')

def logout_account(request):
    logout(request)
    return render(request, 'login.html')

# End Login Logout


#First Time Login
def to_questionaire_user_profile(request):
    if (request.method != 'POST'):
        user_form = UserProfile()
        context = {'user_form': user_form}
        return render(request, 'questionaire_user_profile.html', context)
    else:
        user_form = UserProfile(data=request.POST)
        if user_form.is_valid():
            current_user = user_profile.objects.get(user_id=request.user.id)
            current_user.first_name = user_form.cleaned_data.get('first_name')
            current_user.last_name = user_form.cleaned_data.get('last_name')
            current_user.company_name = user_form.cleaned_data.get('company_name')
            current_user.company_industry = user_form.cleaned_data.get('company_industry')
            current_user.email = user_form.cleaned_data.get('email')
            current_user.address_1 = user_form.cleaned_data.get('address_1')
            current_user.address_2 = user_form.cleaned_data.get('address_2')
            current_user.zip_code = user_form.cleaned_data.get('zip_code')
            current_user.city = user_form.cleaned_data.get('city')
            current_user.user_profile_updated = True
            current_user.save()
            return redirect('/dashboard')

def to_end_user_agreement(request):
    return render(request, 'end_user_agreement.html')

def user_agreed(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    current_user.user_agreement = True
    current_user.save()
    return redirect('/questionaire/user-profile')

def financial_data_questionaire(request):
    if (request.method == 'POST'):
        jsn = json.loads(request.body)
        jsn2 = json.dumps(jsn)
        return JsonResponse(jsn2, safe=False)
    else:
        return render(request, 'financial_data_questionaire.html')

def report_payment(request):
    if (request.method == 'GET'):
        stripe_config = {
            'publicKey' : settings.STRIPE_TEST_PUBLIC_KEY
        }
        return JsonResponse(stripe_config, safe=False)

def report_checkout(request):
    if (request.method == 'GET'):
        domain_url = 'https://pepehands.net:8000/'
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Detailed Report',
                        'quantity': 1,
                        'currency': 'myr',
                        'amount': '10000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def payment_success(request):
    for charges in Charge.api_list():
        Charge.sync_from_stripe_data(charges)
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')





