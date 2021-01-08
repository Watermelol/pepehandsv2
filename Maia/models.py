from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class industries(models.Model):
    industry_name = models.CharField('Industry Name', max_length=255)
    def __str__(self):
        return self.industry_name

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

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)
    instance.user_profile.save()

class user_financial_data(models.Model):
    quaters = [
        ('Q1', 'Quater 1'),
        ('Q2', 'Quater 2'),
    ]

    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now_add=True)
    quater = models.CharField('Quater', choices=quaters, max_length=50, default='Q1')
    revenue = models.FloatField('Revenue')
    net_profit = models.FloatField('Net Profit')
    expenses = models.FloatField('Expenses')
    return_on_equity = models.FloatField('Return On Equity')
    firm_value = models.FloatField('Firm Value')
    debt = models.FloatField('Debt')
    equity = models.FloatField('Equity')
    return_on_asset = models.FloatField('Return On Asset')
    return_on_investment = models.FloatField('Return On Investment')
    networking_capital = models.FloatField('Networking Capital')
    spending_on_research = models.FloatField('Spending On Research')
    property_plant_equipment = models.FloatField('Property Plant Equipment')
    cash_flow = models.FloatField('Cash Flow')
    goodwill = models.FloatField('Goodwill')
    total_assets = models.FloatField('Total Assets')
    total_liabilities = models.FloatField('Total Liabilities')
    current_ratio = models.FloatField('Current Ratio')
    quick_ratio = models.FloatField('Quick Ratio')
    cash_ratio = models.FloatField('Cash Ratio')

    def __str__(self):
        return ('(User ID ' + str(self.user.id) +')' + ' ' + self.user.first_name + ' ' + self.user.last_name + ' ' + self.quater)

class Suggestions(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    URL = models.CharField(max_length = 255)
    Title = models.CharField(max_length = 255)
    Tag = models.CharField(max_length = 255)
    Types = models.CharField(max_length = 10)

class News(models.Model):
    Title = models.CharField(max_length = 50)
    Date = models.DateField()
    Tag = modelsCharField(max_length = 255)
    Categories = models.CharField(max_length = 50)
    Site = models.CharField(max_length = 25)
    URL = models.CharField(max_length = 255)

class News_Sentiment_Analysis(models.Model):
    NewsID = models.ForeignKey(News, on_delete = models.CASCADE)
    Sentiment = models.CharField(max_length = 50)

class Transactions(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    Payment_Status = models.CharField(max_length = 1)
    Amount = models.DecimalField(max_digits = 3, decimal_place = 2)
    Currency = models.CharField(max_length = 5)
    Signature = models.CharField(max_length = 100)
    ErrorDesc = models.IntegerField()
    AuthCode = models.CharField(max_length = 20)
    UsersLoginID = models.CharField(max_length = 10)
    Date = models.DateField()

class Advices(models.Model):
    Text = models.CharField(max_length = 255)
    Tag = models.CharField(max_length = 255)

class Network_Suggestions(models.Model):
    Name = models.CharField(max_length = 50)
    Skills = models.CharField(max_length = 255)
    URL = models.CharField(max_length = 255)
    Tag = models.CharField(max_length = 255)

class Comment(models.Model):
    Text = models.CharField(max_length = 255)
    Tags = models.CharField(max_length = 50)