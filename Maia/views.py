from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import *
from .forms import UserProfile
from djstripe.models import Charge
import json
import stripe
from datetime import date
from .create_report import createReport
from .youtubeAPI import retrive_youtube_videos
from news_processor import *
import datetime

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
            current_user.company_size = user_form.cleaned_data.get('company_size')
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
        jsn = json.loads(request.body)
        current_user = user_profile.objects.get(user_id=request.user.id)
        result = {
            'internalisation': jsn['internalisation'],
            'investment': jsn['investment'],
            'innovation': jsn['innovation'],
            'integration': jsn['integration'],
            'internationalisation': jsn['internationalisation'],
        }
        
        qualitative_questionaire_result = qualitative_result(
            user = current_user,
            internalisation= jsn['internalisation'],
            investment= jsn['investment'],
            innovation= jsn['innovation'],
            integration= jsn['integration'],
            internationalisation= jsn['internationalisation'],
        )

        qualitative_questionaire_answer = qualitative_answer(
            user = current_user,
            set1q1 = jsn['set1'][0],
            set1q2 = jsn['set1'][1],
            set1q3 = jsn['set1'][2],
            set1q4 = jsn['set1'][3],
            set1q5 = jsn['set1'][4],
            set2q1 = jsn['set2'][0],
            set2q2 = jsn['set2'][1],
            set2q3 = jsn['set2'][2],
            set2q4 = jsn['set2'][3],
            set2q5 = jsn['set2'][4],
            set3q1 = jsn['set3'][0],
            set3q2 = jsn['set3'][1],
            set3q3 = jsn['set3'][2],
            set3q4 = jsn['set3'][3],
            set3q5 = jsn['set3'][4],
            set4q1 = jsn['set4'][0],
            set4q2 = jsn['set4'][1],
            set4q3 = jsn['set4'][2],
            set4q4 = jsn['set4'][3],
            set4q5 = jsn['set4'][4],
            set5q1 = jsn['set5'][0],
            set5q2 = jsn['set5'][1],
            set5q3 = jsn['set5'][2],
            set5q4 = jsn['set5'][3],
            set5q5 = jsn['set5'][4],
        )
        
        highest_number = max(result, key=jsn.get)
        
        if (highest_number == 'internalisation'):
            current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Internalisation')

        elif (highest_number == 'investment'):
            current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Investment')

        elif (highest_number == 'innovation'):
            current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Innovation')

        elif (highest_number == 'integration'):
            current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Integration')

        elif (highest_number == 'internationalisation'):
            current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Internationalisation')


        qualitative_questionaire_result.save()
        qualitative_questionaire_answer.save()
        current_user.qualitative_data_provided = True
        current_user.save()
        return HttpResponse("data saved", status=200)
zz
def news_setiment_page(request):
    return render (request, 'news_sentiment.html')


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
            q1_net_cash_flow =int(jsn["q1_net_cash_flow"]),
            q2_revenue = int(jsn["q2_revenue"]),
            q2_profit_before_tax= int(jsn["q2_profit_before_tax"]),
            q2_net_profit= int(jsn["q2_net_profit"]),
            q2_net_cash_flow =int(jsn["q2_net_cash_flow"]),
            q3_revenue = int(jsn["q3_revenue"]),
            q3_profit_before_tax= int(jsn["q3_profit_before_tax"]),
            q3_net_profit= int(jsn["q3_net_profit"]),
            q3_net_cash_flow =int(jsn["q3_net_cash_flow"]),
            q4_revenue = int(jsn["q4_revenue"]),
            q4_profit_before_tax= int(jsn["q4_profit_before_tax"]),
            q4_net_profit= int(jsn["q4_net_profit"]),
            q4_net_cash_flow =int(jsn["q4_net_cash_flow"]),

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
            total_liability = int(jsn['total_liability']),
            shareholder_equity = int(jsn['shareholder_equity']),
            return_on_equity = int(jsn['return_on_equity']),
            )

            


        financial_data_entry.save()


        current_user = user_profile.objects.get(user_id=request.user.id)
        financial_data_me = user_financial_data_v2.objects.get(user=current_user)


        profit_score = profit_cal(financial_data_me)
        asset_score = asset_cal(financial_data_me)
        liquidity_score = liquidity_cal(financial_data_me)
        cash_score = cash_cal(financial_data_me)
        expert_score = (cash_score + liquidity_score + asset_score + profit_score)/4

        analysis_entry = user_financial_data_analysis(
           user = current_user,
            profit_result = profit_score,
            asset_result = asset_score,
            liquidity_result = liquidity_score,
            cash_result = cash_score,
            general_result = expert_score
        )
        analysis_entry.save()

        financial_score_me = user_financial_data_analysis.objects.get(user=current_user)

        #PROFITS TAGGING
        if (financial_score_me.profit_result <= 1.9):
            current_user.profit_tag.add(7)
        elif (financial_score_me.profit_result >= 2 and financial_score_me.profit_result <= 3):
            current_user.profit_tag.add(8)
        elif (financial_score_me.profit_result >= 3.1 and financial_score_me.profit_result <= 4.8):
            current_user.profit_tag.add(9)
        else:
            current_user.profit_tag.add(10)

        if (financial_data_me.q1_net_profit >= financial_data_me.q4_net_profit):
            current_user.profit_tag.add(18)
        else:
            current_user.profit_tag.add(17)

        if (financial_data_me.return_on_equity <= 10):
            current_user.profit_tag.add(11)
        else:
            current_user.profit_tag.add(12)

        if (current_user.company_industry.industry_name == 'Services'):
            if (financial_data_me.return_on_asset <= 6):
                current_user.profit_tag.add(13)
            else:
                current_user.profit_tag.add(14)
        else:
            if (financial_data_me.return_on_asset <= -2.6):
                current_user.profit_tag.add(15)
            else:
                current_user.profit_tag.add(16)
        current_user.profit_tag.remove(1)




        #ASSET TAGGING
        if (financial_score_me.asset_result <= 2.0):
            current_user.asset_tag.add(2)
        elif (financial_score_me.asset_result >= 2.1 and financial_score_me.asset_result <= 4.5):
            current_user.asset_tag.add(3)
        elif (financial_score_me.asset_result >= 4.6 and financial_score_me.asset_result <= 6.2):
            current_user.asset_tag.add(4)
        else:
            current_user.asset_tag.add(5)

        if (current_user.company_industry.industry_name == 'Services'):
            if (financial_data_me.return_on_asset <= 6):
                current_user.asset_tag.add(6)
            else:
                current_user.asset_tag.add(7)
        else:
            if (financial_data_me.return_on_asset <= -2.6):
                current_user.asset_tag.add(8)
            else:
                current_user.asset_tag.add(9)


        if (current_user.company_industry.industry_name == 'Services'):
            if (financial_data_me.asset_turn_over_ratio <= 0.9):
                current_user.asset_tag.add(12)
            else:
                current_user.asset_tag.add(13)
        else:
            if (financial_data_me.asset_turn_over_ratio <= 4.1):
                current_user.asset_tag.add(10)
            else:
                current_user.asset_tag.add(11)


        if (current_user.company_industry.industry_name == 'Services'):
            if (financial_data_me.debt_to_asset_ratio <= 3.7):
                current_user.asset_tag.add(16)
            else:
                current_user.asset_tag.add(17)
        else:
            if (financial_data_me.debt_to_asset_ratio <= 0.49):
                current_user.asset_tag.add(14)
            else:
                current_user.asset_tag.add(15)
        current_user.asset_tag.remove(1)


        #CASH TAGGING
        if (financial_score_me.cash_result <= 3.3):
            current_user.cash_tag.add(2)
        elif (financial_score_me.cash_result >= 3.4 and financial_score_me.cash_result <= 4.4):
            current_user.cash_tag.add(3)
        elif (financial_score_me.cash_result >= 4.5 and financial_score_me.cash_result <= 5.4):
            current_user.cash_tag.add(4)
        else:
            current_user.cash_tag.add(5)

        if (financial_data_me.cash_ratio <= 0.19):
            current_user.cash_tag.add(6)
        else:
            current_user.cash_tag.add(7)

        if (financial_data_me.cash_turnover_ratio <= 1.99):
            current_user.cash_tag.add(8)
        else:
            current_user.cash_tag.add(9)

        if (financial_data_me.q1_net_cash_flow >= financial_data_me.q4_net_cash_flow):
            current_user.cash_tag.add(11)
        else:
            current_user.cash_tag.add(10)
        current_user.cash_tag.remove(1)


        #LIQUIDITY TAG
        if (financial_score_me.liquidity_result <= 4.4):
            current_user.liquidity_tag.add(2)
        elif (financial_score_me.liquidity_result >= 4.5 and financial_score_me.liquidity_result <= 5.7):
            current_user.liquidity_tag.add(3)
        elif (financial_score_me.liquidity_result >= 5.8 and financial_score_me.liquidity_result <= 7.0):
            current_user.liquidity_tag.add(4)
        else:
            current_user.liquidity_tag.add(5)

        if (financial_data_me.current_ratio <= 0.99):
            current_user.liquidity_tag.add(6)
        else:
            current_user.liquidity_tag.add(7)

        if (financial_data_me.quick_ratio <= 0.99):
            current_user.liquidity_tag.add(8)
        else:
            current_user.liquidity_tag.add(9)

        if (financial_data_me.cash_ratio <= 0.19):
            current_user.liquidity_tag.add(10)
        else:
            current_user.liquidity_tag.add(11)
        current_user.liquidity_tag.remove(1)


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






def profit_cal(user_financial_me):
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

def liquidity_cal(user_financial_me):
    NTA = user_financial_me.net_tangeble_asset
    CR = user_financial_me.current_ratio
    Cash_Ratio = user_financial_me.cash_ratio
    QR = user_financial_me.quick_ratio
    Cash = user_financial_me.cash

    result = get_liquidity_predictions(NTA, CR, Cash_Ratio, QR, Cash)

    return result

def cash_cal(user_financial_me):
    Cash_Ratio = user_financial_me.cash_ratio
    CR = user_financial_me.current_ratio
    NTA = user_financial_me.net_tangeble_asset
    Y_NP = user_financial_me.yearly_net_profit
    Debt = user_financial_me.debt
    CTR = user_financial_me.cash_turnover_ratio
    Cash = user_financial_me.cash

    result = get_cash_predictions(Cash_Ratio, CR, NTA, Y_NP, Debt, CTR, Cash)

    return result

def asset_cal(user_financial_me):
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
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    now = date.today()
    dt_string = now.strftime("%d-%m-%Y")
    for charges in Charge.api_list():
        Charge.sync_from_stripe_data(charges)
    fileName = current_user.first_name + current_user.last_name + dt_string + '.pdf'

    data = {
        'profit': {
            'comments': [],
            'suggestions': [],
            'chartsData': {
                'profit': [financial_data.q1_net_profit, financial_data.q2_net_profit, financial_data.q3_net_profit, financial_data.q4_net_profit],
                'revenue': [financial_data.q1_revenue, financial_data.q2_revenue, financial_data.q3_revenue, financial_data.q4_revenue],
            }
        },

        'asset': {
            'comments': [],
            'suggestions': [],
            'chartsData': {
                'return_of_asset': financial_data.return_on_asset,
                'asset_turnover_ratio': financial_data.asset_turn_over_ratio,
                'debt_to_asset_ratio': financial_data.debt_to_asset_ratio,
            }
        },

        'cash': {
            'comments': [],
            'suggestions': [],
            'chartsData': {
                'q1_net_cash_flow': financial_data.q1_net_cash_flow,
                'q2_net_cash_flow': financial_data.q2_net_cash_flow,
                'q3_net_cash_flow': financial_data.q3_net_cash_flow,
                'q4_net_cash_flow': financial_data.q4_net_cash_flow,
            }
        },

        'liquidity': {
            'comments': [],
            'suggestions': [],
            'chartsData': {
                'quick_ratio': financial_data.quick_ratio,
                'current_ratio': financial_data.current_ratio,
                'cash_ratio': financial_data.cash_ratio,
            }
        } 
    }

    current_user_tag_profit = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    for tag in current_user_tag_profit:
        profit_comment = Comment.objects.filter(profit_tag = tag)
        for comment in profit_comment:
            data['profit']['comments'].append(comment.Text)

    for tag in current_user_tag_profit:
        profit_suggestion = Advices.objects.filter(profit_tag = tag)
    
        for suggestion in profit_suggestion:
            data['profit']['suggestions'].append(suggestion.Text)

    current_user_tag_asset = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    for tag in current_user_tag_asset:
        asset_comment = Comment.objects.filter(asset_tag = tag)
        for comment in asset_comment:
            data['asset']['comments'].append(comment.Text)

    for tag in current_user_tag_asset:
        asset_suggestion = Advices.objects.filter(asset_tag = tag)
        for suggestion in asset_suggestion:
            data['asset']['suggestions'].append(suggestion.Text)

    current_user_tag_cash = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    for tag in current_user_tag_cash:
        cash_comment = Comment.objects.filter(cash_tag = tag)
        for comment in cash_comment:
            data['cash']['comments'].append(comment.Text)

    for tag in current_user_tag_cash:
        cash_suggestion = Advices.objects.filter(cash_tag = tag)
        for suggestion in cash_suggestion:
            data['cash']['suggestions'].append(suggestion.Text)

    current_user_tag_liquidity = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    for tag in current_user_tag_liquidity:
        liquidity_comment = Comment.objects.filter(liquidity_tag = tag)
        for comment in liquidity_comment:
            data['liquidity']['comments'].append(comment.Text)

    for tag in current_user_tag_liquidity:
        profit_suggestion = Advices.objects.filter(liquidity_tag = tag)
        for suggestion in profit_suggestion:
            data['liquidity']['suggestions'].append(suggestion.Text)


    createReport(fileName, data)
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
        'company_size_value': current_user.get_company_size_display(),
        'company_size': current_user.company_size,
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
    current_user.company_size = jsn['company_size']
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
        'q1_revenue': financial_data.q1_revenue,
        'q1_profit_before_tax': financial_data.q1_profit_before_tax,
        'q1_net_profit': financial_data.q1_net_profit,
        'q1_net_cash_flow': financial_data.q1_net_cash_flow,
        'q2_revenue': financial_data.q2_revenue,
        'q2_profit_before_tax': financial_data.q2_profit_before_tax,
        'q2_net_profit': financial_data.q2_net_profit,
        'q2_net_cash_flow': financial_data.q2_net_cash_flow,
        'q3_revenue': financial_data.q3_revenue,
        'q3_profit_before_tax': financial_data.q3_profit_before_tax,
        'q3_net_profit': financial_data.q3_net_profit,
        'q3_net_cash_flow': financial_data.q3_net_cash_flow,
        'q4_net_profit': financial_data.q4_net_profit,
        'q4_revenue': financial_data.q4_revenue,
        'q4_profit_before_tax': financial_data.q4_profit_before_tax,
        'q4_net_cash_flow': financial_data.q4_net_cash_flow,
        'yearly_revenue': financial_data.yearly_revenue,
        'yearly_net_profit': financial_data.yearly_net_profit,
        'cash': financial_data.cash,
        'debt': financial_data.debt,
        'total_debt': financial_data.total_debt,
        'net_assets': financial_data.net_assets,
        'current_ratio': financial_data.current_ratio,
        'quick_ratio': financial_data.quick_ratio,
        'cash_ratio': financial_data.cash_ratio,
        'return_on_asset': financial_data.return_on_asset,
        'asset_turn_over_ratio': financial_data.asset_turn_over_ratio,
        'debt_to_asset_ratio': financial_data.debt_to_asset_ratio,
        'net_tangeble_asset': financial_data.net_tangeble_asset,
        'total_liability': financial_data.total_liability,
        'shareholder_equity': financial_data.shareholder_equity,
        'return_on_equity': financial_data.return_on_equity,
    }
    return JsonResponse(jsn_data, safe=False)

def update_user_financial_data(request):
    jsn = json.loads(request.body)
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data_v2.objects.get(user=current_user)

    financial_data.q1_revenue = int(jsn["q1_revenue"])
    financial_data.q1_profit_before_tax= int(jsn["q1_profit_before_tax"])
    financial_data.q1_net_profit= int(jsn["q1_net_profit"])
    financial_data.q1_net_cash_flow= int(jsn["q1_net_cash_flow"])
    financial_data.q2_revenue = int(jsn["q2_revenue"])
    financial_data.q2_profit_before_tax= int(jsn["q2_profit_before_tax"])
    financial_data.q2_net_profit= int(jsn["q2_net_profit"])
    financial_data.q2_net_cash_flow= int(jsn["q2_net_cash_flow"])
    financial_data.q3_revenue = int(jsn["q3_revenue"])
    financial_data.q3_profit_before_tax= int(jsn["q3_profit_before_tax"])
    financial_data.q3_net_profit= int(jsn["q3_net_profit"])
    financial_data.q3_net_cash_flow= int(jsn["q3_net_cash_flow"])
    financial_data.q4_revenue = int(jsn["q4_revenue"])
    financial_data.q4_profit_before_tax= int(jsn["q4_profit_before_tax"])
    financial_data.q4_net_profit= int(jsn["q4_net_profit"])
    financial_data.q4_net_cash_flow= int(jsn["q4_net_cash_flow"])

    financial_data.yearly_revenue = int(jsn['yearly_revenue'])
    financial_data.yearly_net_profit = int(jsn["yearly_net_profit"])
    financial_data.cash = int(jsn['cash'])
    financial_data.debt= int(jsn["debt"])
    financial_data.total_debt = int(jsn['total_debt'])
    financial_data.net_assets = int(jsn["net_assets"])
    financial_data.current_ratio = jsn['current_ratio']
    financial_data.quick_ratio= jsn["quick_ratio"]
    financial_data.cash_ratio = jsn['cash_ratio']
    financial_data.return_on_asset= jsn["return_on_asset"] 
    financial_data.asset_turn_over_ratio = jsn['asset_turn_over_ratio']
    financial_data.debt_to_asset_ratio= jsn["debt_to_asset_ratio"] 
    financial_data.net_tangeble_asset = jsn['net_tangeble_asset']
    financial_data.total_liability = jsn['total_liability']
    financial_data.shareholder_equity= jsn["shareholder_equity"] 
    financial_data.return_on_equity = jsn['return_on_equity']

    financial_data.save()

    financial_data_me = user_financial_data_v2.objects.get(user=current_user)

    profit_score = profit_cal(financial_data_me)
    asset_score = asset_cal(financial_data_me)
    liquidity_score = liquidity_cal(financial_data_me)
    cash_score = cash_cal(financial_data_me)
    expert_score = (cash_score + liquidity_score + asset_score + profit_score)/4

    analysis_entry = user_financial_data_analysis.objects.get(user=current_user)
    analysis_entry.profit_result = profit_score
    analysis_entry. asset_result = asset_score
    analysis_entry.liquidity_result = liquidity_score
    analysis_entry.cash_result = cash_score
    analysis_entry.general_result = expert_score

    analysis_entry.save()

    financial_score_me = user_financial_data_analysis.objects.get(user=current_user)

    #PROFIT TAGGING
    if (financial_score_me.profit_result <= 1.9):
        current_user.profit_tag.add(7)
    elif (financial_score_me.profit_result >= 2 and financial_score_me.profit_result <= 3):
        current_user.profit_tag.add(8)
    elif (financial_score_me.profit_result >= 3.1 and financial_score_me.profit_result <= 4.8):
        current_user.profit_tag.add(9)
    else:
        current_user.profit_tag.add(10)

    if (financial_data_me.q1_net_profit >= financial_data_me.q4_net_profit):
        current_user.profit_tag.add(18)
    else:
        current_user.profit_tag.add(17)

    if (financial_data_me.return_on_equity <= 10):
        current_user.profit_tag.add(11)
    else:
        current_user.profit_tag.add(12)

    if (current_user.company_industry.industry_name == 'Services'):
        if (financial_data_me.return_on_asset <= 6):
            current_user.profit_tag.add(13)
        else:
            current_user.profit_tag.add(14)
    else:
        if (financial_data_me.return_on_asset <= -2.6):
            current_user.profit_tag.add(15)
        else:
            current_user.profit_tag.add(16)
    current_user.profit_tag.remove(1)

            # ASSET TAGGING
    if (financial_score_me.asset_result <= 2.0):
         current_user.asset_tag.add(2)
    elif (financial_score_me.asset_result >= 2.1 and financial_score_me.asset_result <= 4.5):
        current_user.asset_tag.add(3)
    elif (financial_score_me.asset_result >= 4.6 and financial_score_me.asset_result <= 6.2):
        current_user.asset_tag.add(4)
    else:
        current_user.asset_tag.add(5)

    if (current_user.company_industry.industry_name == 'Services'):
        if (financial_data_me.return_on_asset <= 6):
            current_user.asset_tag.add(6)
        else:
            current_user.asset_tag.add(7)
    else:
        if (financial_data_me.return_on_asset <= -2.6):
            current_user.asset_tag.add(8)
        else:
            current_user.asset_tag.add(9)

    if (current_user.company_industry.industry_name == 'Services'):
        if (financial_data_me.asset_turn_over_ratio <= 0.9):
            current_user.asset_tag.add(12)
        else:
            current_user.asset_tag.add(13)
    else:
        if (financial_data_me.asset_turn_over_ratio <= 4.1):
            current_user.asset_tag.add(10)
        else:
            current_user.asset_tag.add(11)

    if (current_user.company_industry.industry_name == 'Services'):
        if (financial_data_me.debt_to_asset_ratio <= 3.7):
            current_user.asset_tag.add(16)
        else:
            current_user.asset_tag.add(17)
    else:
        if (financial_data_me.debt_to_asset_ratio <= 0.49):
            current_user.asset_tag.add(14)
        else:
            current_user.asset_tag.add(15)
    current_user.asset_tag.remove(1)

    # CASH TAGGING
    if (financial_score_me.cash_result <= 3.3):
        current_user.cash_tag.add(2)
    elif (financial_score_me.cash_result >= 3.4 and financial_score_me.cash_result <= 4.4):
        current_user.cash_tag.add(3)
    elif (financial_score_me.cash_result >= 4.5 and financial_score_me.cash_result <= 5.4):
        current_user.cash_tag.add(4)
    else:
        current_user.cash_tag.add(5)

    if (financial_data_me.cash_ratio <= 0.19):
        current_user.cash_tag.add(6)
    else:
        current_user.cash_tag.add(7)

    if (financial_data_me.cash_turnover_ratio <= 1.99):
        current_user.cash_tag.add(8)
    else:
        current_user.cash_tag.add(9)

    if (financial_data_me.q1_net_cash_flow >= financial_data_me.q4_net_cash_flow):
        current_user.cash_tag.add(11)
    else:
        current_user.cash_tag.add(10)
    current_user.cash_tag.remove(1)

    # LIQUIDITY TAG
    if (financial_score_me.liquidity_result <= 4.4):
        current_user.liquidity_tag.add(2)
    elif (financial_score_me.liquidity_result >= 4.5 and financial_score_me.liquidity_result <= 5.7):
        current_user.liquidity_tag.add(3)
    elif (financial_score_me.liquidity_result >= 5.8 and financial_score_me.liquidity_result <= 7.0):
        current_user.liquidity_tag.add(4)
    else:
        current_user.liquidity_tag.add(5)

    if (financial_data_me.current_ratio <= 0.99):
        current_user.liquidity_tag.add(6)
    else:
        current_user.liquidity_tag.add(7)

    if (financial_data_me.quick_ratio <= 0.99):
        current_user.liquidity_tag.add(8)
    else:
        current_user.liquidity_tag.add(9)

    if (financial_data_me.cash_ratio <= 0.19):
        current_user.liquidity_tag.add(10)
    else:
        current_user.liquidity_tag.add(11)
    current_user.liquidity_tag.remove(1)

    return HttpResponse("data saved", status=200)

def profit_pillars(request):
    return render(request, 'pillars/profit_pillar.html')

def asset_pillars(request):
    return render(request, 'pillars/asset_pillar.html')

def cash_pillars(request):
    return render(request, 'pillars/cash_pillar.html')

def liquidity_pillars(request):
    return render(request, 'pillars/liquidity_pillar.html')

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



def get_profit_video(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    videos_id = []
    for tag in current_user_tag:
        recommand_videos = Recommandation_Video.objects.filter(profit_tag = tag)
        for video in recommand_videos:
            if video.Video_ID not in videos_id:
                videos_id.append(video.Video_ID)
            
    response = retrive_youtube_videos(videos_id)
    return JsonResponse(response, safe=False)

def get_profit_article(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    articles = []
    for tag in current_user_tag:
        recommand_article = Recommandation_Articles.objects.filter(profit_tag = tag)
        for article in recommand_article:
            jsn = {
                'title': article.Title,
                'description': article.Description,
                'siteName': article.Site_Name,
                'url': article.URL,
            }
            articles.append(jsn)
    response = {
        'data': articles
    }
    return JsonResponse(response, safe=False)

def get_profit_networking(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    peoples = []
    for tag in current_user_tag:
        networking_peoples = Network_Suggestions.objects.filter(profit_tag = tag)
    
        for people in networking_peoples:
            jsn = {
                'name': people.Name,
                'skills': people.Skills,
                'url': people.URL,
                'thumbnails': people.thumbnails
            }
            peoples.append(jsn)
    response = {
        'data': peoples
    }
    return JsonResponse(response, safe=False)

def get_profit_comment(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    comments = []
    for tag in current_user_tag:
        profit_comment = Comment.objects.filter(profit_tag = tag)
        for comment in profit_comment:
            comments.append(comment.Text) 

    response = {
        'data': comments
    }
    return JsonResponse(response, safe=False)

def get_profit_suggestion(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).profit_tag.all()
    suggestions = []
    for tag in current_user_tag:
        profit_suggestion = Advices.objects.filter(profit_tag = tag)
    
        for suggestion in profit_suggestion:
            suggestions.append(suggestion.Text)
    response = {
        'data': suggestions
    }
    return JsonResponse(response, safe=False)

# Get Asset 

def get_asset_video(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    videos_id = []
    for tag in current_user_tag:
        recommand_videos = Recommandation_Video.objects.filter(asset_tag = tag)
        for video in recommand_videos:
            if video.Video_ID not in videos_id:
                videos_id.append(video.Video_ID)
    response = retrive_youtube_videos(videos_id)
    return JsonResponse(response, safe=False)

def get_asset_article(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    articles = []
    for tag in current_user_tag:
        recommand_article = Recommandation_Articles.objects.filter(asset_tag = tag)
        for article in recommand_article:
            jsn = {
                'title': article.Title,
                'description': article.Description,
                'siteName': article.Site_Name,
                'url': article.URL,
            }
            articles.append(jsn)
    response = {
        'data': articles
    }
    return JsonResponse(response, safe=False)

def get_asset_networking(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    peoples = []
    for tag in current_user_tag:
        networking_peoples = Network_Suggestions.objects.filter(asset_tag = tag)
        for people in networking_peoples:
            jsn = {
                'name': people.Name,
                'skills': people.Skills,
                'url': people.URL,
                'thumbnails': people.thumbnails
            }
            peoples.append(jsn)
    response = {
        'data': peoples
    }
    return JsonResponse(response, safe=False)

def get_asset_comment(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    comments = []
    for tag in current_user_tag:
        profit_comment = Comment.objects.filter(asset_tag = tag)
        for comment in profit_comment:
            comments.append(comment.Text)
    response = {
        'data': comments
    }
    return JsonResponse(response, safe=False)

def get_asset_suggestion(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).asset_tag.all()
    suggestions = []
    for tag in current_user_tag:
        profit_suggestion = Advices.objects.filter(asset_tag = tag)
        for suggestion in profit_suggestion:
            suggestions.append(suggestion.Text)
    response = {
        'data': suggestions
    }
    return JsonResponse(response, safe=False)

# get Cash

def get_cash_video(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    videos_id = []
    for tag in current_user_tag:
        recommand_videos = Recommandation_Video.objects.filter(cash_tag = tag)
        for video in recommand_videos:
            if video.Video_ID not in videos_id:
                videos_id.append(video.Video_ID)
    response = retrive_youtube_videos(videos_id)
    return JsonResponse(response, safe=False)

def get_cash_article(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    articles = []
    for tag in current_user_tag:
        recommand_article = Recommandation_Articles.objects.filter(cash_tag = tag)
        for article in recommand_article:
            jsn = {
                'title': article.Title,
                'description': article.Description,
                'siteName': article.Site_Name,
                'url': article.URL,
            }
            articles.append(jsn)
    response = {
        'data': articles
    }
    return JsonResponse(response, safe=False)

def get_cash_networking(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    peoples = []
    for tag in current_user_tag:
        networking_peoples = Network_Suggestions.objects.filter(cash_tag = tag)
        for people in networking_peoples:
            jsn = {
                'name': people.Name,
                'skills': people.Skills,
                'url': people.URL,
                'thumbnails': people.thumbnails
            }
            peoples.append(jsn)
    response = {
        'data': peoples
    }
    return JsonResponse(response, safe=False)

def get_cash_comment(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    comments = []
    for tag in current_user_tag:
        profit_comment = Comment.objects.filter(cash_tag = tag)
        for comment in profit_comment:
            comments.append(comment.Text)
    response = {
        'data': comments
    }
    return JsonResponse(response, safe=False)

def get_cash_suggestion(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).cash_tag.all()
    suggestions = []
    for tag in current_user_tag:
        profit_suggestion = Advices.objects.filter(cash_tag = tag)
        for suggestion in profit_suggestion:
            suggestions.append(suggestion.Text)
    response = {
        'data': suggestions
    }
    return JsonResponse(response, safe=False)

#  get Liquidity

def get_liquidity_video(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    videos_id = []
    for tag in current_user_tag:
        recommand_videos = Recommandation_Video.objects.filter(liquidity_tag = tag)
        for video in recommand_videos:
            if video.Video_ID not in videos_id:
                videos_id.append(video.Video_ID)
    response = retrive_youtube_videos(videos_id)
    return JsonResponse(response, safe=False)

def get_liquidity_article(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    articles = []
    for tag in current_user_tag:
        recommand_article = Recommandation_Articles.objects.filter(liquidity_tag = tag)
        for article in recommand_article:
            jsn = {
                'title': article.Title,
                'description': article.Description,
                'siteName': article.Site_Name,
                'url': article.URL,
            }
            articles.append(jsn)
    response = {
        'data': articles
    }
    return JsonResponse(response, safe=False)

def get_liquidity_networking(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    peoples = []
    for tag in current_user_tag:
        networking_peoples = Network_Suggestions.objects.filter(liquidity_tag = tag)
        for people in networking_peoples:
            jsn = {
                'name': people.Name,
                'skills': people.Skills,
                'url': people.URL,
                'thumbnails': people.thumbnails
            }
            peoples.append(jsn)
    response = {
        'data': peoples
    }
    return JsonResponse(response, safe=False)

def get_liquidity_comment(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    comments = []
    for tag in current_user_tag:
        profit_comment = Comment.objects.filter(liquidity_tag = tag)
        for comment in profit_comment:
            comments.append(comment.Text)
    response = {
        'data': comments
    }
    return JsonResponse(response, safe=False)

def get_liquidity_suggestion(request):
    current_user_tag = user_profile.objects.get(user_id=request.user.id).liquidity_tag.all()
    suggestions = []
    for tag in current_user_tag:
        profit_suggestion = Advices.objects.filter(liquidity_tag = tag)
        for suggestion in profit_suggestion:
            suggestions.append(suggestion.Text)
    response = {
        'data': suggestions
    }
    return JsonResponse(response, safe=False)

def get_analysis_result(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    analysis_result = user_financial_data_analysis.objects.get(user= current_user)
    response = {
        'overallScore': analysis_result.general_result,
        'profitabilityScore': analysis_result.profit_result,
        'assetScore': analysis_result.asset_result,
        'cashScore': analysis_result.cash_result,
        'liquidityScore': analysis_result.liquidity_result
    }

    return JsonResponse(response, safe=False)

def get_profit_chart_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    response = {
        'profit': [financial_data.q1_net_profit, financial_data.q2_net_profit, financial_data.q3_net_profit, financial_data.q4_net_profit],
        'revenue': [financial_data.q1_revenue, financial_data.q2_revenue, financial_data.q3_revenue, financial_data.q4_revenue],
    }

    return JsonResponse(response, safe=False)

def get_asset_chart_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    response = {
        'return_of_asset': financial_data.return_on_asset,
        'asset_turnover_ratio': financial_data.asset_turn_over_ratio,
        'debt_to_asset_ratio': financial_data.debt_to_asset_ratio,
    }

    return JsonResponse(response, safe=False)
    
# News sentiment handling
def get_news_sentiment(request):
    import pickle

    # Get industry
    current_user = user_profile.objects.get(user_id = request.user.id)
    file_name =  "Maia/News_Sentiment/" + current_user.company_industry.industry_name + ".pkl"

    # Open pickle file
    pickle_file = open(file_name, "rb")
    while True:
        try:
            news_list = pickle.load(pickle_file)
        except EOFError:
            break
    pickle_file.close()

    # Average scores
    average_sentiment_score = 0
    average_sentiment_magitude = 0
    for news_var in news_list:
        average_sentiment_score += news_var.emotion_score
        average_sentiment_magitude += news_var.emotion_strength

    average_sentiment_score /= len(news_list)
    average_sentiment_magitude /= len(news_list)

    # Magnitude has a score from 0 to infinite
    # Assign emotion strength
    classification = ""
    if average_sentiment_magitude >= 5:
        classification = "Strongly "

    # Score has a score from -1 to 1
    # Assign score emotion
    if average_sentiment_score >= 0.25:
        classification += "Positive "
    elif average_sentiment_score <= -0.25:
        classification += "Negative "
    else:
        classification += "Neutral "

    # For loop to list out news_list
    news_number = 1
    news_array = []
    for tempNews in news_list:
        if news_number <= 20:
            score_word = ''
            magnitude_word = ''
            if tempNews.emotion_score >= 0.25:
                score_word += "Positive"
            elif tempNews.emotion_score <= -0.25:
                score_word += "Negative"
            else:
                score_word += "Neutral"

            if tempNews.emotion_strength >= 5:
                magnitude_word = 'Strongly'
            
            news_array.append({
                'news_title': tempNews.title,
                'url': tempNews.url,
                'date': tempNews.date_published,
                'epoch': datetime.datetime.strptime(tempNews.date_published, '%Y-%m-%dT%H:%M:%S').timestamp(),
                'emotion_score': tempNews.emotion_score,
                'emotion_score_word': score_word,
                'emotion_strength': tempNews.emotion_strength,
                'emotion_strength_word': magnitude_word,
                'emotion_classification': tempNews.emotion_classification
            })
            news_number += 1
        else:
            break

    # Build the response
    response = {
        'overallSentimentScore': average_sentiment_score,
        'overallMagnitude': average_sentiment_magitude,
        'sentimentClassification': classification,
        'newsList': news_array
    }

    return JsonResponse(response, safe = False)

def get_cash_chart_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    response = {
        'q1_net_cash_flow': financial_data.q1_net_cash_flow,
        'q2_net_cash_flow': financial_data.q2_net_cash_flow,
        'q3_net_cash_flow': financial_data.q3_net_cash_flow,
        'q4_net_cash_flow': financial_data.q4_net_cash_flow,
    }

    return JsonResponse(response, safe=False)

def get_liquidity_chart_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    financial_data = user_financial_data_v2.objects.get(user=current_user)
    response = {
        'quick_ratio': financial_data.quick_ratio,
        'current_ratio': financial_data.current_ratio,
        'cash_ratio': financial_data.cash_ratio,
    }

    return JsonResponse(response, safe=False)

def get_questionaire_data(request):
    current_user = user_profile.objects.get(user_id=request.user.id)
    user_questionaire_answer = qualitative_answer.objects.get(user = current_user)
    response = {
        'set1q1': user_questionaire_answer.set1q1,
        'set1q2': user_questionaire_answer.set1q2,
        'set1q3': user_questionaire_answer.set1q3,
        'set1q4': user_questionaire_answer.set1q4,
        'set1q5': user_questionaire_answer.set1q5,
        'set2q1': user_questionaire_answer.set2q1,
        'set2q2': user_questionaire_answer.set2q2,
        'set2q3': user_questionaire_answer.set2q3,
        'set2q4': user_questionaire_answer.set2q4,
        'set2q5': user_questionaire_answer.set2q5,
        'set3q1': user_questionaire_answer.set3q1,
        'set3q2': user_questionaire_answer.set3q2,
        'set3q3': user_questionaire_answer.set3q3,
        'set3q4': user_questionaire_answer.set3q4,
        'set3q5': user_questionaire_answer.set3q5,
        'set4q1': user_questionaire_answer.set4q1,
        'set4q2': user_questionaire_answer.set4q2,
        'set4q3': user_questionaire_answer.set4q3,
        'set4q4': user_questionaire_answer.set4q4,
        'set4q5': user_questionaire_answer.set4q5,
        'set5q1': user_questionaire_answer.set5q1,
        'set5q2': user_questionaire_answer.set5q2,
        'set5q3': user_questionaire_answer.set5q3,
        'set5q4': user_questionaire_answer.set5q4,
        'set5q5': user_questionaire_answer.set5q5,
    }

    return JsonResponse(response, safe=False)

def update_user_questionaire_data(request):
    jsn = json.loads(request.body)
    current_user = user_profile.objects.get(user_id=request.user.id)
    user_questionaire_answer = qualitative_answer.objects.get(user = current_user)
    user_questionaire_result = qualitative_result.objects.get(user = current_user)

    user_questionaire_answer.set1q1 = jsn['set1'][0]
    user_questionaire_answer.set1q2 = jsn['set1'][1]
    user_questionaire_answer.set1q3 = jsn['set1'][2]
    user_questionaire_answer.set1q4 = jsn['set1'][3]
    user_questionaire_answer.set1q5 = jsn['set1'][4]
    user_questionaire_answer.set2q1 = jsn['set2'][0]
    user_questionaire_answer.set2q2 = jsn['set2'][1]
    user_questionaire_answer.set2q3 = jsn['set2'][2]
    user_questionaire_answer.set2q4 = jsn['set2'][3]
    user_questionaire_answer.set2q5 = jsn['set2'][4]
    user_questionaire_answer.set3q1 = jsn['set3'][0]
    user_questionaire_answer.set3q2 = jsn['set3'][1]
    user_questionaire_answer.set3q3 = jsn['set3'][2]
    user_questionaire_answer.set3q4 = jsn['set3'][3]
    user_questionaire_answer.set3q5 = jsn['set3'][4]
    user_questionaire_answer.set4q1 = jsn['set4'][0]
    user_questionaire_answer.set4q2 = jsn['set4'][1]
    user_questionaire_answer.set4q3 = jsn['set4'][2]
    user_questionaire_answer.set4q4 = jsn['set4'][3]
    user_questionaire_answer.set4q5 = jsn['set4'][4]
    user_questionaire_answer.set5q1 = jsn['set5'][0]
    user_questionaire_answer.set5q2 = jsn['set5'][1]
    user_questionaire_answer.set5q3 = jsn['set5'][2]
    user_questionaire_answer.set5q4 = jsn['set5'][3]
    user_questionaire_answer.set5q5 = jsn['set5'][4]

    user_questionaire_result.internalisation = jsn['internalisation']
    user_questionaire_result.investment = jsn['investment']
    user_questionaire_result.innovation = jsn['innovation']
    user_questionaire_result.integration = jsn['integration']
    user_questionaire_result.internationalisation = jsn['internationalisation']

    result = {
            'internalisation': jsn['internalisation'],
            'investment': jsn['investment'],
            'innovation': jsn['innovation'],
            'integration': jsn['integration'],
            'internationalisation': jsn['internationalisation'],
    }

    highest_number = max(result, key=jsn.get)
        
    if (highest_number == 'internalisation'):
        current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Internalisation')

    elif (highest_number == 'investment'):
        current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Investment')

    elif (highest_number == 'innovation'):
        current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Innovation')

    elif (highest_number == 'integration'):
        current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Integration')

    elif (highest_number == 'internationalisation'):
        current_user.qualitative_tag = qualitative_tag.objects.get(name = 'Internationalisation')

    user_questionaire_answer.save()
    user_questionaire_result.save()
    current_user.save()

    return HttpResponse("data saved", status=200)

