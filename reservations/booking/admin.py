from django.contrib import admin
from .models import Gare, Trajet , Client, Passager, Reservation
from geoposition.fields import GeopositionField


class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__','telephone', 'adresse', 'user')
    search_fields = ('user__first_name', 'user__last_name','user')
    fieldsets = (
        (None, { 'fields': [ 'prenom', 'nom','user', 'telephone', 'adresse']}),
    )


##Toutes la gestion et les recherches admin sont faites ici
class TrajetAdmin(admin.ModelAdmin):
    list_display = ('__str__','date_depart', 'date_arrivee', 'reservations_par_jour_moy', 'nb_passagers')
    list_filter = ('gare_depart', 'gare_arrivee')
    search_fields = ('gare_depart', 'gare_arrivee')

    ##Déclare la liste de passager comme field pour être lu par Django
    readonly_fields = ('liste_passagers',)
    @admin.display(description="liste des passagers")
    ##Rends un string déjà formatté pour être affiché dans la page admin
    def liste_passagers(self, obj):
            resas = Reservation.objects.filter(trajet=obj)
            passas = ""
            for resa in resas:
                passas = passas + str(resa.passager) + '\n'
            return passas
    fieldsets = (
        (None, { 'fields': ['gare_depart', 'gare_arrivee']}),
        ("Date information", {'fields': ['date_depart','date_arrivee']}), 
        ("Liste des Passagers", {'fields' : ['liste_passagers']})
     
    )
    
    


    

class GareAdmin(admin.ModelAdmin):
    list_filter = ('ville',)
    search_fields = ('nom', 'ville')

    list_display = ('nom', 'ville', 'position', 'freq_totale_pass', 'freq_totale_trajets' )
    class Media:
        js = (
            'geoposition/google.js',  # chemin vers geoposition.js
        )

    

    
class PassagerAdmin(admin.ModelAdmin):
    list_display = ('__str__','date_naissance')
    search_fields = ('nom', 'prenom')
    fieldsets = (
        (None, { 'fields': ['nom', 'prenom','client']}),
        ("Information supplémentaire", {'fields': ['date_naissance']}),
    )
    
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('__str__','date_reservation', 'numero_reservation', 'numero_voiture', 'numero_place')
    search_fields = ('numero_reservation', 'numero_voiture', 'numero_place', 'trajet__gare_depart__nom', 'trajet__gare_arrivee__nom')
    list_filter = ('date_reservation', 'numero_reservation', 'trajet__gare_depart', 'trajet__gare_arrivee', 'trajet')
    fieldsets = (
        (None, { 'fields': ['date_reservation', 'trajet', 'numero_voiture', 'numero_place']}),
        ("Information passager et client", {'fields': ['passager', 'client']}),
    )

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Gare, GareAdmin)
admin.site.register(Trajet, TrajetAdmin)
admin.site.register(Passager, PassagerAdmin)
admin.site.register(Reservation, ReservationAdmin)
