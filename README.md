# reservations-Adam-Benabou


## 1. Descriptif de l'application ##

L'application prénommée booking permet de reserver un trajet en train 

Pour y accéder, aller sur l'url suivant: 
http://localhost:8000/booking/menu 
### 2. Contenu de l'application ##

* Menu principal de navigation [booking/](http://localhost:8000/booking/)
* Liste des trajets [booking/trajets](http://localhost:8000/booking/trajets)
* Interface de connection [booking/accounts/login](http://localhost:8000/booking/account/login)
* Page profil [booking/profil](http://localhost:8000/booking/profil)
* Liste des réservations [booking/reservations](http://localhost:8000/booking/reservations)
* Detail d'une réservation 
* Creation et modification d'une réservation 


NB : L'affichage des pages utilise boostrap et java scripts. La plupart des fonctionalités boostrap et js ont été trouvé sur le web
La page login.html provient majoritairement du tuto sur les logins fourni par Django (avec du boostrap pour la rendre plus stylisée )__

J'ai crée deux templates de base [`menu_auth`](/reservations/booking/templates/booking/menu_auth.html) et [`menu_pas_auth`](/reservations/booking/templates/booking/menu_pas_auth.html) afin que toutes les pages du site internet ait un menu (qui diffère si l'on est connecté ou non) 

NB utilsateur:  benab
   mdp    : djangoadmin 

ce profil à des passagers et des réservations déja enregistrès 

NB 2 : Quand l'admin rajoute des gare , merci de choisir à l'aide de gmaps la gare SNCF ( et non le métro ou l'arrêt de bus à coté ) sinon l'itinéraire prendra en compte d'autres modes de transports.
Petit contretemps : On ne peut créer que des trajets qui sont possibles dans la vraie vie en train. Par exemple , un trajet Gare Montparnasse-Gare de Lyon-Par Dieu est impossible puisque  qu'il faut partir de la gare de Lyon pour pouvoir aller à Lyon... Le service d'itinéraire de gmaps nous fera donc utiliser un autre mode de transports en commun pour atteindre la gare de Lyon 

De plus , j'ai rajouté le date de départ pour que google maps calcule automatiquement le trajet mais cela veut dire que notre base de données doit être réelle !! ( contraignant :( ))