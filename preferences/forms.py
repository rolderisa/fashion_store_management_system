from django import forms
from .models import CustomerPreference
from products.models import Category




class CustomerPreferenceForm(forms.ModelForm):
    class Meta:
        model = CustomerPreference
        fields = ['favorite_category', 'size', 'color', 'receive_notifications', 'preferred_contact_method']
        widgets = {
            'receive_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'preferred_contact_method': forms.Select(attrs={'class': 'form-select'}),
        }


class add(forms.ModelForm):
    class Meta:
        model = CustomerPreference
        fields = ['favorite_category', 'size', 'color', 'receive_notifications', 'preferred_contact_method']

   
    favorite_category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
    size = forms.ChoiceField(choices=[('32', '32'), ('34', '34'), ('36', '36')], required=False)
    color = forms.CharField(max_length=50, required=False)
    receive_notifications = forms.BooleanField(required=False)
    preferred_contact_method = forms.ChoiceField(choices=[('SMS', 'SMS'), ('Email', 'Email')])