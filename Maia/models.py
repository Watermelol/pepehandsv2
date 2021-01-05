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


