from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Passager(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    
class Client(models.Model) : 
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = PhoneNumberField( max_length=15)
    
class Trajet(models.Model):
    gare_depart = models.CharField(max_length=255)
    gare_arrivee = models.CharField(max_length=255)
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    
class Reservation(models.Model):
    date_reservation = models.DateTimeField()
    numero_reservation = models.IntegerField()
    numero_voiture = models.IntegerField()
    numero_place = models.IntegerField()
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    
    
# Create your models here.
