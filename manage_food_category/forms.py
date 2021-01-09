from django import forms

from category_app.models import Category


class FoodCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"Name", 'name': 'name'}))


    class Meta:
        model = Category
        fields = ['name']