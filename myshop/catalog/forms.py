# forms.py
from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    email = forms.EmailField(label='Почта')
