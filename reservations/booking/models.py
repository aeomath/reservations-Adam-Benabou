from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = PhoneNumberField( max_length=15)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    def __str__(self):
        return self.prenom + ' ' + self.nom
    
class Passager(models.Model):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    def __str__(self):
        return self.prenom + ' ' + self.nom

class Gare(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom
    
class Trajet(models.Model):
    gare_depart = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='gare_depart')
    gare_arrivee = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='gare_arrivee')
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    
    ## ne fonctionne pas pour l'instant
    if date_arrivee < date_depart:
        raise ValidationError("La date d'arrivée doit être supérieure à la date de départ")
    ###
    
    
    def __str__(self):
        ## La méthode strftime est utilisée pour convertir un objet datetime en une chaîne de caractères formatée.
        local_date_depart = timezone.localtime(self.date_depart)
        return self.gare_depart.nom + ' - ' + self.gare_arrivee.nom + ' : ' + local_date_depart.strftime(" %d/%m/%Y %H:%M ")
    
    
class Reservation(models.Model):
    date_reservation = models.DateTimeField()
    numero_reservation = models.IntegerField(primary_key=True)
    numero_voiture = models.IntegerField()
    numero_place = models.IntegerField()
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)

    ## rajout de la contrainte d'unicité pour la place par trajet (code trouvé sur le net)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trajet', 'numero_place'], name='unique_place_par_trajet')
        ]
    def __str__(self):
        return str(self.trajet)

    
    

