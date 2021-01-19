from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import user_profile, user_financial_data_v2, user_payment, purchased_report
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
        financial_data_entry = user_financial_data_v2(
            user_id = current_user.id,
            q1_revenue = int(jsn["q1_revenue"]),
            q1_profit_before_tax= int(jsn["q1_profit_before_tax"]),
            q1_net_profit= int(jsn["q1_net_profit"]),
            q2_revenue = int(jsn["q2_revenue"]),
            q2_profit_before_tax= int(jsn["q2_profit_before_tax"]),
            q2_net_profit= int(jsn["q2_net_profit"]),
            q3_revenue = int(jsn["q3_revenue"]),
            q3_profit_before_tax= int(jsn["q3_profit_before_tax"]),
            q3_net_profit= int(jsn["q3_net_profit"]),
            q4_revenue = int(jsn["q4_revenue"]),
            q4_profit_before_tax= int(jsn["q4_profit_before_tax"]),
            q4_net_profit= int(jsn["q4_net_profit"]),


            yearly_revenue = int(jsn['yearly_revenue']),
            yearly_net_profit = int(jsn["yearly_net_profit"]),
            cash = int(jsn['cash']),
            debt= int(jsn["debt"]),
            total_debt = int(jsn['total_debt']),
            net_assets = int(jsn["net_assets"]),
            current_ratio = jsn['current_ratio'],
            quick_ratio= jsn["quick_ratio"], 
            cash_ratio = jsn['cash_ratio'],
            return_on_asset= jsn["return_on_asset"], 
            asset_turn_over_ratio = jsn['asset_turn_over_ratio'],
            debt_to_asset_ratio= jsn["debt_to_asset_ratio"], 
            net_tangeble_asset = jsn['net_tangeble_asset'],

            q1_net_profit_margin = int(jsn['q1_net_profit'])/int(jsn['q1_revenue']),
            q2_net_profit_margin=int(jsn['q2_net_profit'])/int(jsn['q2_revenue']),
            q3_net_profit_margin=int(jsn['q3_net_profit'])/int(jsn['q3_revenue']),
            q4_net_profit_margin=int(jsn['q4_net_profit'])/int(jsn['q4_revenue']),
            yearly_net_profit_margin = int(jsn['yearly_net_profit'])/int(jsn['yearly_revenue']),
            cash_turnover_ratio = int(jsn['yearly_revenue'])/int(jsn['cash']),
        )



        financial_data_entry.save()
        financial_data_me = user_financial_data_v2.objects.get(user = current_user)
        # gets the current user financial data

        pp = profit_result(financial_data_me)
        ap = asset_result(financial_data_me)
        lp = liquidity_result(financial_data_me)
        cp = cash_result(financial_data_me)

        print(pp)
        print(ap)
        print(lp)
        print(cp)


        #ex = expert_result(financial_data_me)
        #print(ex)


        # pass the data to machinelearning and get the result


        # store the result into database

        current_user.financial_data_provided = True
        current_user.save()
        return HttpResponse("data saved", status=200)


        
def get_expert_predictions(ROA, NA, NTA, CR, Q1_NP, DTA):
    import pickle
    model = pickle.load(open("Maia/Expert_Score_Model.sav", "rb"))
    prediction = model.predict([[ROA, NA, NTA, CR, Q1_NP, DTA]])
    return prediction


def get_profit_predictions(ROA, Y_NP, NTA, Q1_NPM, Q2_NPM, Q3_NPM, Q4_NPM, YNPM, CTR):
    import pickle
    model = pickle.load(open("Maia/Profit_Score_Model.sav", "rb"))
    profit_prediction = model.predict([[ROA, Y_NP, NTA, Q1_NPM, Q2_NPM, Q3_NPM, Q4_NPM, YNPM, CTR]])
    return profit_prediction

def get_liquidity_predictions(NTA, CR, Cash_Ratio, QR, Cash):
    import pickle
    model = pickle.load(open("Maia/Liquidity_Score_Model.sav", "rb"))
    liquidity_prediction = model.predict([[NTA, CR, Cash_Ratio, QR, Cash]])
    return liquidity_prediction

def get_cash_predictions(Cash_Ratio, CR, NTA, Y_NP, Debt, CTR, Cash):
    import pickle
    model = pickle.load(open("Maia/Cash_Score_Model.sav", "rb"))
    cash_prediction =  model.predict([[Cash_Ratio, CR, NTA, Y_NP, Debt, CTR, Cash]])
    return cash_prediction

def get_asset_predictions(YNPM, ATR, DTA, ROA, Cash_Ratio, QR, CR, NA, NTA, Debt, TD, Y_R, Y_NP):
    import pickle
    model = pickle.load(open("Maia/Asset_Score_Model.sav", "rb"))
    asset_prediction = model.predict([[YNPM, ATR, DTA, ROA, Cash_Ratio, QR, CR, NA, NTA, Debt, TD, Y_R, Y_NP]])
    return asset_prediction



#def expert_result(user_financial_me):
   # ROA = user_financial_me.return_on_asset
   # NA = user_financial_me.net_assets
   # NTA = user_financial_me.net_tangeble_asset
   # CR = user_financial_me.current_ratio
   # Q1_NP = user_financial_me.q1_net_profit
   # DTA = user_financial_me.debt_to_asset_ratio

    #result = get_expert_predictions(ROA, NA, NTA, CR, Q1_NP, DTA)

    #return result


def profit_result(user_financial_me):
    ROA = user_financial_me.return_on_asset
    Y_NP = user_financial_me.yearly_net_profit
    NTA = user_financial_me.net_tangeble_asset
    Q1_NPM = user_financial_me.q1_net_profit_margin
    Q2_NPM = user_financial_me.q2_net_profit_margin
    Q3_NPM = user_financial_me.q3_net_profit_margin
    Q4_NPM = user_financial_me.q4_net_profit_margin
    YNPM = user_financial_me.yearly_net_profit_margin
    CTR = user_financial_me.cash_turnover_ratio

    result = get_profit_predictions(ROA, Y_NP, NTA, Q1_NPM, Q2_NPM, Q3_NPM, Q4_NPM, YNPM, CTR)

    return result

def liquidity_result(user_financial_me):
    NTA = user_financial_me.net_tangeble_asset
    CR = user_financial_me.current_ratio
    Cash_Ratio = user_financial_me.cash_ratio
    QR = user_financial_me.quick_ratio
    Cash = user_financial_me.cash

    result = get_liquidity_predictions(NTA, CR, Cash_Ratio, QR, Cash)

    return result

def cash_result(user_financial_me):
    Cash_Ratio = user_financial_me.cash_ratio
    CR = user_financial_me.current_ratio
    NTA = user_financial_me.net_tangeble_asset
    Y_NP = user_financial_me.yearly_net_profit
    Debt = user_financial_me.debt
    CTR = user_financial_me.cash_turnover_ratio
    Cash = user_financial_me.cash

    result = get_cash_predictions(Cash_Ratio, CR, NTA, Y_NP, Debt, CTR, Cash)

    return result

def asset_result(user_financial_me):
    YNPM = user_financial_me.yearly_net_profit_margin
    ATR = user_financial_me.asset_turn_over_ratio
    DTA = user_financial_me.debt_to_asset_ratio
    ROA = user_financial_me.return_on_asset
    Cash_Ratio = user_financial_me.cash_ratio
    QR = user_financial_me.quick_ratio
    CR = user_financial_me.current_ratio
    NA = user_financial_me.net_assets
    NTA = user_financial_me.net_tangeble_asset
    Debt = user_financial_me.debt
    TD = user_financial_me.total_debt
    Y_R = user_financial_me.yearly_revenue
    Y_NP = user_financial_me.yearly_net_profit

    result = get_asset_predictions(YNPM, ATR, DTA, ROA, Cash_Ratio, QR, CR, NA, NTA, Debt, TD, Y_R, Y_NP)

    return result







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
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    jsn_data = {
        'q1_revenue': financial_data.q1_revenue / 1000,
        'q1_profit_before_tax': financial_data.q1_profit_before_tax / 1000,
        'q1_net_profit': financial_data.q1_net_profit / 1000,
        'q2_revenue': financial_data.q2_revenue / 1000,
        'q2_profit_before_tax': financial_data.q2_profit_before_tax / 1000,
        'q2_net_profit': financial_data.q2_net_profit / 1000,
        'q3_revenue': financial_data.q3_revenue / 1000,
        'q3_profit_before_tax': financial_data.q3_profit_before_tax / 1000,
        'q3_net_profit': financial_data.q3_net_profit / 1000,
        'q4_net_profit': financial_data.q4_net_profit / 1000,
        'q4_revenue': financial_data.q4_revenue / 1000,
        'q4_profit_before_tax': financial_data.q4_profit_before_tax / 1000,
        'yearly_revenue': financial_data.yearly_revenue / 1000,
        'yearly_net_profit': financial_data.yearly_net_profit / 1000,
        'cash': financial_data.cash / 1000,
        'debt': financial_data.debt / 1000,
        'total_debt': financial_data.total_debt / 1000,
        'net_assets': financial_data.net_assets / 1000,
        'current_ratio': financial_data.current_ratio,
        'quick_ratio': financial_data.quick_ratio,
        'cash_ratio': financial_data.cash_ratio,
        'return_on_asset': financial_data.return_on_asset,
        'asset_turn_over_ratio': financial_data.asset_turn_over_ratio,
        'debt_to_asset_ratio': financial_data.debt_to_asset_ratio,
        'net_tangeble_asset': financial_data.net_tangeble_asset,
    }
    return JsonResponse(jsn_data, safe=False)

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
    financial_data = user_financial_data_v2.objects.get(user=current_user)

    financial_data.q1_revenue = int(jsn["q1_revenue"]) * 1000
    financial_data.q1_profit_before_tax= int(jsn["q1_profit_before_tax"]) * 1000
    financial_data.q1_net_profit= int(jsn["q1_net_profit"]) * 1000
    financial_data.q2_revenue = int(jsn["q2_revenue"]) * 1000
    financial_data.q2_profit_before_tax= int(jsn["q2_profit_before_tax"]) * 1000
    financial_data.q2_net_profit= int(jsn["q2_net_profit"]) * 1000
    financial_data.q3_revenue = int(jsn["q3_revenue"]) * 1000
    financial_data.q3_profit_before_tax= int(jsn["q3_profit_before_tax"]) * 1000
    financial_data.q3_net_profit= int(jsn["q3_net_profit"]) * 1000
    financial_data.q4_revenue = int(jsn["q4_revenue"]) * 1000
    financial_data.q4_profit_before_tax= int(jsn["q4_profit_before_tax"]) * 1000
    financial_data.q4_net_profit= int(jsn["q4_net_profit"]) * 1000

    financial_data.yearly_revenue = int(jsn['yearly_revenue']) * 1000
    financial_data.yearly_net_profit = int(jsn["yearly_net_profit"]) * 1000
    financial_data.cash = int(jsn['cash']) * 1000
    financial_data.debt= int(jsn["debt"]) * 1000
    financial_data.total_debt = int(jsn['total_debt']) * 1000
    financial_data.net_assets = int(jsn["net_assets"]) * 1000
    financial_data.current_ratio = jsn['current_ratio']
    financial_data.quick_ratio= jsn["quick_ratio"]
    financial_data.cash_ratio = jsn['cash_ratio']
    financial_data.return_on_asset= jsn["return_on_asset"] 
    financial_data.asset_turn_over_ratio = jsn['asset_turn_over_ratio']
    financial_data.debt_to_asset_ratio= jsn["debt_to_asset_ratio"] 
    financial_data.net_tangeble_asset = jsn['net_tangeble_asset']

    financial_data.save()
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











