from django import forms
from django import forms
from .models import Gare, Trajet, Passager, Reservation, Client
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    gare_depart = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    gare_arrivee = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    


class ReservationForm(forms.ModelForm):
    ## on surcharge la méthode __init__ pour pouvoir passer un client en paramètre et pouvoir filtrer les passagers
    def __init__(self, client = None , *args, **kwargs):
        super(ReservationForm, self).__init__(*args , **kwargs)
        if client:
            self.fields['passager'].queryset = Passager.objects.filter(client=client)
    class Meta:
        model = Reservation
        fields = ['trajet','numero_voiture','numero_place','passager']

class Register_Client(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)
    
    class Meta:
        model = Client
        fields = ['prenom', 'nom','adresse','telephone', 'username','password']
