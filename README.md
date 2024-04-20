# reservations-Adam-Benabou


## 1. Descriptif de l'application ##

L'application prénommée booking permet de reserver un trajet en train 

Pour y accéder, aller sur l'url suivant: 
http://localhost:8000/booking/menu 
### 2. Contenu de l'application ##

* Menu principal de navigation [booking/menu](http://localhost:8000/booking/menu)
* Liste des trajets [booking/menu](http://localhost:8000/booking/trajets)
* Interface de connection [booking/accounts/login](http://localhost:8000/booking/account/login)
* Page profil [booking/profil](http://localhost:8000/booking/profil)
* Liste des réservations [booking/reservations](http://localhost:8000/booking/reservations)
* Detail d'une réservation 
* Creation et modification d'une réservation 


NB : L'affichage des pages utilise boostrap et java scripts. La plupart des fonctionalités boostrap et js ont été trouvé sur le web
La page login.html provient majoritairement du tuto sur les logins fourni par Django (avec du boostrap pour la rendre plus stylisée )__

J'ai crée deux templates de base [`menu_auth`](/reservations/booking/templates/booking/menu_auth.html) et [`menu_pas_auth`](/reservations/booking/templates/booking/menu_pas_auth.html) afin que toutes les pages du site internet ait un menu (qui diffère si l'on est connecté ou non) 
