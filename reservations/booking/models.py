from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


'''
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
    

'''

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
    
    def __str__(self):
        return self.gare_depart.nom + ' - ' + self.gare_arrivee.nom
    
    
'''
class Reservation(models.Model):
    date_reservation = models.DateTimeField()
    numero_reservation = models.IntegerField()
    numero_voiture = models.IntegerField()
    numero_place = models.IntegerField()
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
'''

    
    
# Create your models here.
