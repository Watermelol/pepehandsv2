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

    # Four pillars
    path('pillars/performance', views.performance_pillars , name='performance_pillars'),
    path('pillars/business-value', views.business_value_pillars , name='business_value_pillars'),
    path('pillars/productivity', views.productivity_pillars , name='productivity_pillars'),
    path('pillars/risk-analysis', views.risk_analysis_pillars , name='risk_analysis_pillars'),

]
