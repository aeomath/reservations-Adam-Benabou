from django import forms
from django import forms
from .models import Gare, Trajet


class SearchForm(forms.Form):
    gare_depart = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    gare_arrivee = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)