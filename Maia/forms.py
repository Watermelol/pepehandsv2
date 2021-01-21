from django import forms
from .models import user_profile

class UserProfile (forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ['first_name', 'last_name', 'email', 'address_1', 'address_2', 'zip_code', 'city', 'company_name', 'company_industry', 'company_size']