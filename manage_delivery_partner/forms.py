from django import forms
from .models import Delivery_Partner
# --------------------------------------------------------------------

# Sign Up Form
class DeliveryPartnerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"Name", 'name': 'name'}))
    deep_link_url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"Deep Link URL", 'name': 'deep_link_url'}))

    class Meta:
        model = Delivery_Partner
        fields = ['name','deep_link_url']
