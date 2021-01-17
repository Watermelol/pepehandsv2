from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from djstripe.models import Charge as Strip_Charge
import json


# Create your models here.

class industries(models.Model):
    industry_name = models.CharField('Industry Name', max_length=255)
    def __str__(self):
        return self.industry_name

class tag (models.Model):
    name = models.CharField('Name', max_length=255, default='')
    desc = models.CharField('Description', max_length=255, default='')
    def __str__(self):
        return self.name

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=255, default='')
    last_name = models.CharField('Last Name', max_length=255, default='')
    company_name = models.CharField('Company Name', max_length=255, default='')
    company_industry = models.ForeignKey(industries, on_delete=models.RESTRICT, default=1 ,verbose_name='Company Industry')
    email = models.EmailField(default='')
    address_1 = models.CharField('Address 1', max_length=255, default='')
    address_2 = models.CharField('Address 2', max_length=255, default='', blank=True, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12, default='')
    city = models.CharField("City", max_length=1024, default='')
    user_agreement = models.BooleanField(default=False)
    user_profile_updated = models.BooleanField(default=False)
    financial_data_provided = models.BooleanField(default=False)
    qualitative_data_provided = models.BooleanField(default=False)
    tag = models.ManyToManyField(tag, default=1 ,verbose_name='Tag')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)
    instance.user_profile.save()

class user_payment(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    payment_record = models.OneToOneField(Strip_Charge, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.payment_record.id + ')'

@receiver(post_save, sender=Strip_Charge)
def create_payment_record(sender, instance, created, **kwargs):
    if created:
        billingDetails = instance.billing_details
        current_user = user_profile.objects.get(email=billingDetails['email'])
        current_user_payment = user_payment.objects.create(user=current_user, payment_record=instance)
        current_user_payment.save()

class user_financial_data_v2(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now_add=True)
    q1_revenue = models.FloatField('Q1 Revenue')
    q1_profit_before_tax = models.FloatField('Q1 Profit Before Tax')
    q1_net_profit = models.FloatField('Q1 Net Profit')
    q2_revenue = models.FloatField('Q2 Revenue')
    q2_profit_before_tax = models.FloatField('Q2 Profit Before Tax')
    q2_net_profit = models.FloatField('Q2 Net Profit')
    q3_revenue = models.FloatField('Q3 Revenue')
    q3_profit_before_tax = models.FloatField('Q3 Profit Before Tax')
    q3_net_profit = models.FloatField('Q3 Net Profit')
    q4_revenue = models.FloatField('Q4 Revenue')
    q4_profit_before_tax = models.FloatField('Q4 Profit Before Tax')
    q4_net_profit = models.FloatField('Q4 Net Profit')
    yearly_revenue = models.FloatField('Yearly Revenue')
    yearly_net_profit = models.FloatField('Yearly Net Profit')
    net_tangeble_asset = models.FloatField('Net Tangeble Asset')
    cash = models.FloatField('Cash')
    debt = models.FloatField('Debt')
    total_debt = models.FloatField('Total Debt')
    net_assets = models.FloatField('Net Assets')
    current_ratio = models.FloatField('Current Ratio')
    quick_ratio = models.FloatField('Quick Ratio')
    cash_ratio = models.FloatField('Cash Ratio')
    return_on_asset = models.FloatField('Return On Assest')
    asset_turn_over_ratio = models.FloatField('Asset Turn Over Ratio')
    debt_to_asset_ratio = models.FloatField('Debt To Asset Ratio')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class user_financial_data_analysis(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    profit_result = models.FloatField('Profit Result')
    asset_result = models.FloatField('Asset Result')
    cash_result = models.FloatField('Cash Result')
    liquidity_result = models.FloatField('Liquidity Result')
    general_result = models.FloatField('General Result')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

# class News(models.Model):
#     Title = models.CharField(max_length = 50)
#     Date = models.DateField()
#     Tag = models.CharField(max_length = 255)
#     content_text = models.TextField()
#     Categories = models.CharField(max_length = 50)
#     Site = models.CharField(max_length = 25)
#     URL = models.CharField(max_length = 255)

# class News_Sentiment_Analysis(models.Model):
#     NewsID = models.ForeignKey(News, on_delete = models.CASCADE)
#     Sentiment = models.CharField(max_length = 50)

class Advices(models.Model):
    Text = models.CharField('Text', max_length = 255)
    tag = models.ForeignKey(tag, default=1 ,verbose_name='Tag', on_delete=models.CASCADE)

class Comment(models.Model):
    Text = models.CharField(max_length = 255)
    tag = models.ForeignKey(tag, default=1 ,verbose_name='Tag', on_delete=models.CASCADE)

class Network_Suggestions(models.Model):
    Name = models.CharField(max_length = 50)
    Skills = models.CharField(max_length = 255)
    URL = models.CharField(max_length = 255)
    tag = models.ManyToManyField(tag, default=1 ,verbose_name='Tag')

class Recommandation_Video(models.Model):
    Name = models.CharField(max_length = 50)
    Video_ID = models.CharField(max_length=255)
    tag = models.ManyToManyField(tag, default=1 ,verbose_name='Tag')

class Recommandation_Articles(models.Model):
    Title = models.CharField(max_length = 50)
    Description = models.TextField(blank=True)
    Site_Name = models.CharField(max_length=50)
    URL = models.CharField(max_length = 255)
    tag = models.ManyToManyField(tag, default=1 ,verbose_name='Tag')

class purchased_report(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField('Purchased Date', auto_now_add=True)
    file_name = models.CharField('File Name', max_length=255)

    def __str__(self):
        return (self.file_name)

