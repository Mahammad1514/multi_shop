# forms.py

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class ContactForm(forms.Form):
    pass 