from django.forms import ModelForm
from . import models as clothes_models
from options import models as options_models
from markets import models as markgets_models


class SearchForm(ModelForm):
    class Meta:
        model = clothes_models.Clothes
        fields = ("name",)



class ContactForm(ModelForm):

    class Meta:
        model = clothes_models.Clothes
        fields = '__all__'
    
