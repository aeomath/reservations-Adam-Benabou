from django import forms
from django import forms
from .models import Gare, Trajet, Passager, Reservation, Client
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    gare_depart = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    gare_arrivee = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    
## Pas utilisé pour l'instant  
class PassagerForm(forms.ModelForm):
    class Meta:
        model = Passager
        fields = ['prenom', 'nom','date_naissance'] 

class ReservationForm(forms.ModelForm):
    passager = forms.ModelChoiceField(queryset=Passager.objects.all())
    class Meta:
        model = Reservation
        fields = ['trajet','numero_voiture','numero_place','passager']

class Register_Client(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)
    
    class Meta:
        model = Client
        fields = ['prenom', 'nom','adresse','telephone', 'username','password']
