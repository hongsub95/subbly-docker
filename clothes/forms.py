from django import forms
from . import models as clothes_models
from markets import models as markets_models


class SearchForm(forms.ModelForm):
    class Meta:
        model = clothes_models.Clothes
        fields = ("name",)


class SearchForm(forms.Form):
    clothes = forms.CharField(
        label='검색키워드',
        required=False,
    )


class ContactForm(forms.ModelForm):

    class Meta:
        model = clothes_models.Clothes
        fields = '__all__'
    
