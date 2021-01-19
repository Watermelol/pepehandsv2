"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Maia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.login, name='login'),
    path("logout/", views.logout_account, name="logout"),
    
    # User First Time Login
    path('end-user-agreement/', views.to_end_user_agreement, name="end_user_agreement"),
    path('user-agreeded/', views.user_agreed, name="user_agreed"),
    path('questionaire/user-profile', views.to_questionaire_user_profile, name="questionaire_user_profile"),
    path('financial_data_questionaire/', views.financial_data_questionaire, name="financial_data_questionaire"),
    path('qualitative_questionaire/', views.qualitative_questionaire, name="qualitative_questionaire"),

    # Report Payment
    path('report_payment/', views.report_payment, name="report_payment"),
    path('create-checkout-session/', views.report_checkout),
    path('success/', views.payment_success),
    path('cancelled/', views.payment_cancelled),

    #  Stripr Web
    path("stripe/", include("djstripe.urls", namespace="djstripe")),


    # Social Login
    path('social-auth/', include('social_django.urls', namespace="social")),

    # User Profile Page
    path('user-profile/', views.user_profile_page , name='user_profile'),
    path('user/get/data/', views.get_user_data, name='retrieve_user_data'),
    path('user/get/payment_history', views.get_user_payment_history, name='retrieve_user_payment_history'),
    path('user/get/data/', views.get_user_data, name='retrieve_user_data'),
    path('user/update', views.update_user_profile, name='update_user_profile'),
    path('user/get/data/financial', views.get_user_financial_data, name='update_user_profile'),
    path('user/update/data/financial', views.update_user_financial_data, name='update_user_profile'),
    path('user/get/purchased_report', views.get_purchased_report, name='get_purchased_report'),

    # Four pillars
    path('pillars/profit', views.profit_pillars , name='profit_pillars'),
    path('pillars/asset', views.asset_pillars , name='asset_pillars'),
    path('pillars/cash', views.cash_pillars , name='cash_pillars'),
    path('pillars/liquidity', views.liquidity_pillars , name='liquidity_pillars'),
    path('pillars/profit/videos', views.get_profit_video , name='profit_pillars_videos'),
    path('pillars/profit/article', views.get_profit_article , name='profit_pillars_article'),
    path('pillars/profit/networking', views.get_profit_networking , name='profit_pillars_networking'),
    path('pillars/profit/comment', views.get_profit_comment , name='profit_pillars_comment'),
    path('pillars/profit/suggestion', views.get_profit_suggestion , name='profit_pillars_suggestion'),
]
