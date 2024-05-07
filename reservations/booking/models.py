from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
import math
from django.contrib import admin

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
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.prenom + ' ' + self.nom

class Gare(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)

    position = GeopositionField(null=True, default='48.8566,2.3522')
    
    ##Donne la fréquence des trajets par gare
    def freq_totale_trajets(self):
        trajets1 = Trajet.objects.filter(gare_depart=self)
        trajets2 = Trajet.objects.filter(gare_arrivee=self)
        return len(trajets1) + len(trajets2)
    
    ##Donne la fréquence de passagers par gare, compte deux fois les passagers qui font une correspondance
    def freq_totale_pass(self):
        trajets1 = Trajet.objects.filter(gare_depart=self)
        trajets2 = Trajet.objects.filter(gare_arrivee=self)
        nbpassas = 0
        for trajet in trajets1:
            nbpassas += len(Reservation.objects.filter(trajet=trajet))
        for trajet in trajets2:
            nbpassas += len(Reservation.objects.filter(trajet=trajet))
        return nbpassas
    

    def __str__(self):
        return self.nom
    
    
    
class Trajet(models.Model):
    gare_depart = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='gare_depart')
    gare_arrivee = models.ForeignKey(Gare, on_delete=models.CASCADE, related_name='gare_arrivee')
    
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    max_passagers = models.IntegerField(default=10000)
    
    ## ne fonctionne pas pour l'instant
    if date_arrivee < date_depart:
        raise ValidationError("La date d'arrivée doit être supérieure à la date de départ")
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Conversion des degrés en radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Rayon de la terre en kilomètres
        R = 6371.0

        # Différences
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Formule de Haversine
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance
        distance = R * c

        return distance
    

    ## Renvoie un dictionnaire dont les clefs sont un tuple (date, nom_du_trajet_sur_lequel_on_appelle_la_méthode) 
    # et la valeur une liste singleton contenant le nbre de reservations de ce trajet au cours du jour "date"
    def nb_reservations_chaque_jour(self):

        reservations = Reservation.objects.filter(trajet=self).order_by('date_reservation')
        
        res_by_day = {}
        for res in reservations:
            ## res_by_day = {(date,nom_trajet): [nb_res]}
            res_date = res.date_reservation.date()
            key = (res_date, f"{self.gare_depart}=>{self.gare_arrivee}")
            if not(res_date in list(res_by_day.keys())):
                res_by_day[key] = [1]
            else:
                res_by_day[key][0] += 1
        return res_by_day
    
    ## Retourne le nombre de reservations du trajet (self) faites le jour "date"
    def nb_reservations_par_jour(self, date):
        return Reservation.objects.filter(trajet=self, date_reservation__date=date).count()

    
    def reservations_par_jour_moy(self):
        reservations = Reservation.objects.filter(trajet=self).order_by('date_reservation')
        if len(reservations) == 0:
            return 0
        
        avg = len(reservations)/((reservations[len(reservations)-1].date_reservation.date()-reservations[0].date_reservation.date()).days+1)
                
        return avg
    
    ##Donne le nombre de passagers total du trajet
    def nb_passagers(self):
        return len(Reservation.objects.filter(trajet=self))
    


    
    def __str__(self):
        ## La méthode strftime est utilisée pour convertir un objet datetime en une chaîne de caractères formatée.
        local_date_depart = timezone.localtime(self.date_depart)
        return self.gare_depart.nom + ' - ' + self.gare_arrivee.nom + ' : ' + local_date_depart.strftime(" %d/%m/%Y %H:%M ")
    
    
class Reservation(models.Model):
    date_reservation = models.DateTimeField()
    numero_reservation = models.AutoField(primary_key=True)
    numero_voiture = models.IntegerField()
    numero_place = models.IntegerField() ##Ne doit pas dépasser le nombre max de passagers
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)

    ## rajout de la contrainte d'unicité pour la place par trajet (code trouvé sur le net)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trajet', 'numero_place'], name='unique_place_par_trajet'),
        ]
    def __str__(self):
        return str(self.trajet)

    



