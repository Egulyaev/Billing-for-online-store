from django import forms
from django.forms import ModelForm

from main.models import Purchases


class PurchasesForm(ModelForm):
    class Meta:
        model = Purchases
        fields = ('product', 'buyer')


class GetDateForm(forms.Form):
    purchase = forms.DateField(label='Дата покупки (формат YYYY-MM-DD)', )


class GetCategoryForm(forms.Form):
    category = forms.CharField()


class GetProductForm(forms.Form):
    product = forms.CharField()
