from django.urls import path,include

from . import views

urlpatterns = [
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.menu, name="menu"),
    path("trajets/", views.trajets, name="trajets"),
    path("itineraire/", views.itineraire, name="itineraire"),
    path("nouvel_itineraire", views.nouvel_itineraire, name = "nouvelle_reservation_itineraire"),
    path("reservations/", views.reservations, name="reservations"),
    path("reservations/<int:reservation_id>/", views.reservation, name="reservation"),
    path("nouvelle_reservation/", views.edit_reservation, name="nouvelle_reservation"),
    path("nouvelle_reservation/<int:trajet_id>/", views.edit_reservation, name="nouvelle_reservation_trajet"),
    path("modifier_reservation/<int:reservation_id>/", views.edit_reservation, name="modifier_reservation"),
    path("supprimer_reservation/<int:reservation_id>/", views.delete_reservation, name="supprimer_reservation"),
    path("register", views.register, name="register"),
    path("register/<int:client_id>/", views.register, name="edit_profil"),
    path("profil", views.profil, name="profil"),
]