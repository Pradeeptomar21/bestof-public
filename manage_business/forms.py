from django import forms
from business_detail.models import Business_Details
from manage_delivery_partner.models import Delivery_Partner

# --------------------------------------------------------------------

# Sign Up Form
class BusinessDeliveryPartnerForm(forms.ModelForm):
    dilevery_partner = forms.ModelMultipleChoiceField(queryset=Delivery_Partner.objects.all(),widget=forms.SelectMultiple(attrs={"class": "form-control",'placeholder':"Dileviery Partner", 'name': 'dilevery_partner'}))

    class Meta:
        model = Business_Details
        fields = ['dilevery_partner']
