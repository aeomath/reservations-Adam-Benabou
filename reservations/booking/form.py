from django import forms
from django import forms
from .models import Gare, Trajet, Passager, Reservation


class SearchForm(forms.Form):
    gare_depart = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    gare_arrivee = forms.ModelChoiceField(queryset=Gare.objects.all(), required=False)
    
    
class PassagerForm(forms.ModelForm):
    class Meta:
        model = Passager
        fields = ['prenom', 'nom','date_naissance'] 

class ReservationForm(forms.ModelForm):
    passager = forms.ModelChoiceField(queryset=Passager.objects.all())
    class Meta:
        model = Reservation
        fields = ['trajet','numero_voiture','numero_place','passager']