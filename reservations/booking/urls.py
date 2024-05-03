from django.urls import path,include

from . import views

urlpatterns = [
    ##menu
    path("", views.menu, name="menu"),
    ## authentification et profil
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register, name="register"),
    path("register/<int:client_id>/", views.register, name="edit_profil"),
    path("profil", views.profil, name="profil"),
    path("create_passager", views.create_passager, name="create_passager"),
    ## trajets (urls publics)
    path("trajets/", views.trajets, name="trajets"),
    ## reservations (urls privés)
    path("reservations/", views.reservations, name="reservations"),
    path("reservations/<int:reservation_id>/", views.reservation, name="reservation"),
    path("nouvelle_reservation/", views.edit_reservation, name="nouvelle_reservation"),
    path("nouvelle_reservation/<int:trajet_id>/", views.edit_reservation, name="nouvelle_reservation_trajet"),
    path("modifier_reservation/<int:reservation_id>/", views.edit_reservation, name="modifier_reservation"),
    path("supprimer_reservation/<int:reservation_id>/", views.delete_reservation, name="supprimer_reservation"),
]