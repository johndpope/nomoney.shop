""" forms of the search module """
from django import forms


class SearchForm(forms.Form):
    """ form of the submitted search string """
    text = forms.CharField(max_length=300)
