from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import user_profile, user_financial_data, user_payment, purchased_report
from .forms import UserProfile
from djstripe.models import Charge
import json
import stripe
from datetime import datetime
from .create_report import createReport

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
            elif (qualitative_data_provided != True):
                return redirect('/qualitative_questionaire')
            # if user answer b4 then redirect him to dashboard else bring him to questionaire page
            else:
                return render(request, 'dashboard.html')

# Login Logout
def login(request):
    # check if the user is log in ady or not
    if request.user.is_authenticated:
        return redirect('dashboard/')
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

def qualitative_questionaire(request):
    if (request.method != 'POST'):
        return render(request, 'qualitative_questionaire.html')
    else:
        current_user = user_profile.objects.get(user_id=request.user.id)
        current_user.qualitative_data_provided = True
        current_user.save()
        return HttpResponse("data saved", status=200)


def financial_data_questionaire(request):
    if (request.method != 'POST'):
        return render(request, 'financial_data_questionaire.html')
    else:
        jsn = json.loads(request.body)
        current_user = user_profile.objects.get(user_id=request.user.id)
        current_user_id = current_user.user_id
        # print(jsn["data"])
        for financial_data in jsn["data"]:
            financial_data_entry = user_financial_data(
                user_id = current_user.id,
                quater = financial_data["quater"],
                revenue = financial_data["revenue"],
                net_profit= financial_data["net_profit"],
                expenses= financial_data["expenses"],
                return_on_equity= financial_data["return_on_equity"],
                firm_value= financial_data["firm_value"],
                debt= financial_data["debt"],
                equity= financial_data["equity"],
                return_on_asset= financial_data["return_on_asset"],
                return_on_investment= financial_data["return_on_investment"],
                networking_capital= financial_data["networking_capital"],
                spending_on_research= financial_data["spending_on_research"],
                property_plant_equipment= financial_data["property_plant_equipment"],
                cash_flow= financial_data["cash_flow"],
                goodwill= financial_data["goodwill"],
                total_assets= financial_data["total_assets"],
                total_liabilities= financial_data["total_liabilities"],
                current_ratio= financial_data["current_ratio"],
                quick_ratio= financial_data["quick_ratio"],
                cash_ratio= financial_data["cash_ratio"]
            )

            financial_data_entry.save()
        
        
        current_user.financial_data_provided = True
        current_user.save()
        return HttpResponse("data saved", status=200)
        

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
    current_user = user_profile.objects.get(user_id=request.user.id)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    for charges in Charge.api_list():
        Charge.sync_from_stripe_data(charges)
    fileName = current_user.first_name + current_user.last_name + dt_string + '.pdf'
    createReport(fileName)
    report_purchased = purchased_report(
        user = current_user,
        file_name = fileName
    )

    report_purchased.save()
    context={'fileName': fileName}
    return render(request, 'payment_success.html', context)

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def user_profile_page(request):
    return render(request, 'user_profile_page.html')

def get_user_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    current_user_profile = {
        'firstName': current_user.first_name,
        'lastName': current_user.last_name,
        'companyName': current_user.company_name,
        'company_industry': current_user.company_industry.industry_name,
        'email': current_user.email,
        'address1': current_user.address_1,
        'address2': current_user.address_2,
        'city': current_user.city,
        'zipCode': current_user.zip_code,
    }

    return JsonResponse(current_user_profile, safe=False)

def get_user_payment_history(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    current_user_payment_history = user_payment.objects.filter(user = current_user)
    payment_history_data = []
    for data in current_user_payment_history:
        jsn_data = {
            'charges': data.payment_record.amount,
            'currency': data.payment_record.currency,
            'created': str(data.payment_record.created)
        }
        payment_history_data.append(jsn_data)
    response_jsn = {
        'data': payment_history_data
    }
    return JsonResponse(response_jsn, safe=False)

def update_user_profile(request):
    jsn = json.loads(request.body)
    current_user = user_profile.objects.get(user_id=request.user.id)
    current_user.first_name = jsn['firstName']
    current_user.last_name = jsn['lastName']
    current_user.company_name = jsn['companyName']
    current_user.email = jsn['email']
    current_user.address_1 = jsn['address1']
    current_user.address_2 = jsn['address2']
    current_user.zip_code = jsn['zipCode']
    current_user.city = jsn['city']
    current_user.save()

    return HttpResponse("data saved", status=200)

def get_user_financial_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data.objects.filter(user=current_user)
    response_arry = []
    data_size = 1
    for data in financial_data:
        jsn_data = {
            'id': data_size,
            'quater' : data.quater,
            'revenue' : data.revenue,
            'net_profit' : data.net_profit,
            'expenses' : data.expenses,
            'return_on_equity' : data.return_on_equity,
            'firm_value' : data.firm_value,
            'debt' : data.debt,
            'equity' : data.equity,
            'return_on_asset' : data.return_on_asset,
            'return_on_investment' : data.return_on_investment,
            'networking_capital' : data.networking_capital,
            'spending_on_research' : data.spending_on_research,
            'property_plant_equipment' : data.property_plant_equipment,
            'cash_flow' : data.cash_flow,
            'goodwill' : data.goodwill,
            'total_assets' : data.total_assets,
            'total_liabilities' : data.total_liabilities,
            'current_ratio' : data.current_ratio,
            'quick_ratio' : data.quick_ratio,
            'cash_ratio' : data.cash_ratio,
        }
        response_arry.append(jsn_data)
        data_size += 1

    response_jsn = {
        'data': response_arry
    }
    return JsonResponse(response_jsn, safe=False)

# def update_user_profile(request):
#     jsn = json.loads(request.body)
#     current_user = user_profile.objects.get(user_id=request.user.id)
#     current_user.first_name = jsn['firstName']
#     current_user.last_name = jsn['lastName']
#     current_user.company_name = jsn['companyName']
#     current_user.email = jsn['email']
#     current_user.address_1 = jsn['address1']
#     current_user.address_2 = jsn['address2']
#     current_user.zip_code = jsn['zipCode']
#     current_user.city = jsn['city']
#     current_user.save()

#     return HttpResponse("data saved", status=200)

def update_user_financial_data(request):
    jsn = json.loads(request.body)
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data.objects.filter(user=current_user)
    for data in financial_data:
        for k in jsn['data']:
            if(k['quater'] == 'Q1' and data.quater == 'Q1'):
                data.revenue = k['revenue']
                data.net_profit = k['net_profit']
                data.expenses = k['expenses']
                data.return_on_equity = k['return_on_equity']
                data.firm_value = k['firm_value']
                data.debt = k['debt']
                data.equity = k['equity']
                data.return_on_asset = k['return_on_asset']
                data.return_on_investment = k['return_on_investment']
                data.networking_capital = k['networking_capital']
                data.spending_on_research = k['spending_on_research']
                data.property_plant_equipment = k['property_plant_equipment']
                data.cash_flow = k['cash_flow']
                data.goodwill = k['goodwill']
                data.total_assets = k['total_assets']
                data.total_liabilities = k['total_liabilities']
                data.current_ratio = k['current_ratio']
                data.quick_ratio = k['quick_ratio']
                data.quick_ratio = k['quick_ratio']

            elif(k['quater'] == 'Q2' and data.quater == 'Q2'):
                data.revenue = k['revenue']
                data.net_profit = k['net_profit']
                data.expenses = k['expenses']
                data.return_on_equity = k['return_on_equity']
                data.firm_value = k['firm_value']
                data.debt = k['debt']
                data.equity = k['equity']
                data.return_on_asset = k['return_on_asset']
                data.return_on_investment = k['return_on_investment']
                data.networking_capital = k['networking_capital']
                data.spending_on_research = k['spending_on_research']
                data.property_plant_equipment = k['property_plant_equipment']
                data.cash_flow = k['cash_flow']
                data.goodwill = k['goodwill']
                data.total_assets = k['total_assets']
                data.total_liabilities = k['total_liabilities']
                data.current_ratio = k['current_ratio']
                data.quick_ratio = k['quick_ratio']
                data.quick_ratio = k['quick_ratio']
        
        data.save()
    return HttpResponse("data saved", status=200)

def performance_pillars(request):
    return render(request, 'pillars/performance_pillar.html')

def business_value_pillars(request):
    return render(request, 'pillars/business_value_pillar.html')

def productivity_pillars(request):
    return render(request, 'pillars/productivity_pillar.html')

def risk_analysis_pillars(request):
    return render(request, 'pillars/risk_analysis_pillar.html')

def get_purchased_report(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    report_purchased = purchased_report.objects.filter(user=current_user)
    respond_arry = []
    for data in report_purchased:
        jsn = {
            'purchaseDate': str(data.purchased_date),
            'fileName': data.file_name
        }
        respond_arry.append(jsn)
    respond_jsn = {
        'data': respond_arry
    }

    return JsonResponse(respond_jsn, safe=False)











