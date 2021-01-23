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

# class tag (models.Model):
#     name = models.CharField('Name', max_length=255, default='')
#     desc = models.CharField('Description', max_length=255, default='')
#     def __str__(self):
#         return self.name

class tag_profit (models.Model):
    name = models.CharField('Name', max_length=255, default='')
    min_result = models.FloatField(default=0.00)
    max_result = models.FloatField(default=0.00)
    desc = models.CharField('Description', max_length=255, default='', blank=True)
    def __str__(self):
        return self.name

class tag_asset (models.Model):
    name = models.CharField('Name', max_length=255, default='')
    min_result = models.FloatField(default=0.00)
    max_result = models.FloatField(default=0.00)
    desc = models.CharField('Description', max_length=255, default='', blank=True)
    def __str__(self):
        return self.name

class tag_cash (models.Model):
    name = models.CharField('Name', max_length=255, default='')
    min_result = models.FloatField(default=0.00)
    max_result = models.FloatField(default=0.00)
    desc = models.CharField('Description', max_length=255, default='', blank=True)
    def __str__(self):
        return self.name

class tag_liquidity (models.Model):
    name = models.CharField('Name', max_length=255, default='')
    min_result = models.FloatField(default=0.00)
    max_result = models.FloatField(default=0.00)
    desc = models.CharField('Description', max_length=255, default='', blank=True)
    def __str__(self):
        return self.name

class user_profile(models.Model):
    COMPANY_SIZE = [
    ('MC', 'Micro'),
    ('SM', 'Small'),
    ('MD', 'Medium'),
]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=255, default='')
    last_name = models.CharField('Last Name', max_length=255, default='')
    company_name = models.CharField('Company Name', max_length=255, default='')
    company_industry = models.ForeignKey(industries, on_delete=models.RESTRICT, default=1 ,verbose_name='Company Industry')
    email = models.EmailField(default='')
    company_size = models.CharField(max_length=5, choices=COMPANY_SIZE, default='SM')
    address_1 = models.CharField('Address 1', max_length=255, default='')
    address_2 = models.CharField('Address 2', max_length=255, default='', blank=True, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12, default='')
    city = models.CharField("City", max_length=1024, default='')
    user_agreement = models.BooleanField(default=False)
    user_profile_updated = models.BooleanField(default=False)
    financial_data_provided = models.BooleanField(default=False)
    qualitative_data_provided = models.BooleanField(default=False)
    profit_tag = models.ManyToManyField(tag_profit, default=1, verbose_name='Profit Tag')
    asset_tag = models.ManyToManyField(tag_asset, default=1, verbose_name='Asset Tag')
    cash_tag = models.ManyToManyField(tag_cash, default=1, verbose_name='Cash Tag')
    liquidity_tag = models.ManyToManyField(tag_liquidity, default=1, verbose_name='Liquidity Tag')

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
    q1_net_cash_flow = models.FloatField('Q1 Net Cash Flow')
    q2_revenue = models.FloatField('Q2 Revenue')
    q2_profit_before_tax = models.FloatField('Q2 Profit Before Tax')
    q2_net_profit = models.FloatField('Q2 Net Profit')
    q2_net_cash_flow = models.FloatField('Q2 Net Cash Flow')
    q3_revenue = models.FloatField('Q3 Revenue')
    q3_profit_before_tax = models.FloatField('Q3 Profit Before Tax')
    q3_net_profit = models.FloatField('Q3 Net Profit')
    q3_net_cash_flow = models.FloatField('Q2 Net Cash Flow')
    q4_revenue = models.FloatField('Q4 Revenue')
    q4_profit_before_tax = models.FloatField('Q4 Profit Before Tax')
    q4_net_profit = models.FloatField('Q4 Net Profit')
    q4_net_cash_flow = models.FloatField('Q2 Net Cash Flow')
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
    q1_net_profit_margin = models.FloatField('Q1 Net Profit Margin')
    q2_net_profit_margin = models.FloatField('Q2 Net Profit Margin')
    q3_net_profit_margin = models.FloatField('Q3 Net Profit Margin')
    q4_net_profit_margin = models.FloatField('Q4 Net Profit Margin')
    yearly_net_profit_margin = models.FloatField('Yearly Net Profit Margin')
    cash_turnover_ratio = models.FloatField('Cash Turnover Ratio')
    total_liability = models.FloatField('Total Liability', default=0)
    shareholder_equity = models.FloatField('Shareholder Equity', default=0)
    return_on_equity = models.FloatField('Return on Equity', default=0)

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
    Text = models.TextField()
    profit_tag = models.ForeignKey(tag_profit, default=1, on_delete=models.RESTRICT, verbose_name='Profit Tag')
    asset_tag = models.ForeignKey(tag_asset, default=1, on_delete=models.RESTRICT, verbose_name='Asset Tag')
    cash_tag = models.ForeignKey(tag_cash, default=1, on_delete=models.RESTRICT, verbose_name='Cash Tag')
    liquidity_tag = models.ForeignKey(tag_liquidity, default=1, on_delete=models.RESTRICT, verbose_name='Liquidity Tag')
    def __str__(self):
        return (self.Text)

class Comment(models.Model):
    Text = models.TextField()
    profit_tag = models.ForeignKey(tag_profit, default=1, on_delete=models.RESTRICT, verbose_name='Profit Tag')
    asset_tag = models.ForeignKey(tag_asset, default=1, on_delete=models.RESTRICT, verbose_name='Asset Tag')
    cash_tag = models.ForeignKey(tag_cash, default=1, on_delete=models.RESTRICT, verbose_name='Cash Tag')
    liquidity_tag = models.ForeignKey(tag_liquidity, default=1, on_delete=models.RESTRICT, verbose_name='Liquidity Tag')
    def __str__(self):
        return (self.Text)

class Network_Suggestions(models.Model):
    Name = models.CharField(max_length = 50)
    Skills = models.TextField()
    URL = models.CharField(max_length = 255)
    thumbnails = models.TextField(blank=True)
    profit_tag = models.ForeignKey(tag_profit, default=1, on_delete=models.RESTRICT, verbose_name='Profit Tag')
    asset_tag = models.ForeignKey(tag_asset, default=1, on_delete=models.RESTRICT, verbose_name='Asset Tag')
    cash_tag = models.ForeignKey(tag_cash, default=1, on_delete=models.RESTRICT, verbose_name='Cash Tag')
    liquidity_tag = models.ForeignKey(tag_liquidity, default=1, on_delete=models.RESTRICT, verbose_name='Liquidity Tag')
    def __str__(self):
        return (self.Name)

class Recommandation_Video(models.Model):
    Name = models.TextField()
    Video_ID = models.CharField(max_length=255)
    profit_tag = models.ForeignKey(tag_profit, default=1, on_delete=models.RESTRICT, verbose_name='Profit Tag')
    asset_tag = models.ForeignKey(tag_asset, default=1, on_delete=models.RESTRICT, verbose_name='Asset Tag')
    cash_tag = models.ForeignKey(tag_cash, default=1, on_delete=models.RESTRICT, verbose_name='Cash Tag')
    liquidity_tag = models.ForeignKey(tag_liquidity, default=1, on_delete=models.RESTRICT, verbose_name='Liquidity Tag')

    def __str__(self):
        return (self.Name)

class Recommandation_Articles(models.Model):
    Title = models.TextField()
    Description = models.TextField(blank=True)
    Site_Name = models.CharField(max_length=100)
    URL = models.CharField(max_length = 255)
    profit_tag = models.ForeignKey(tag_profit, default=1, on_delete=models.RESTRICT, verbose_name='Profit Tag')
    asset_tag = models.ForeignKey(tag_asset, default=1, on_delete=models.RESTRICT, verbose_name='Asset Tag')
    cash_tag = models.ForeignKey(tag_cash, default=1, on_delete=models.RESTRICT, verbose_name='Cash Tag')
    liquidity_tag = models.ForeignKey(tag_liquidity, default=1, on_delete=models.RESTRICT, verbose_name='Liquidity Tag')

    def __str__(self):
        return (self.Title)

class purchased_report(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField('Purchased Date', auto_now_add=True)
    file_name = models.CharField('File Name', max_length=255)

    def __str__(self):
        return (self.file_name)

