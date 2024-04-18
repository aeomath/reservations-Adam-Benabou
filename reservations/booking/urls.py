from django.urls import path,include

from . import views

urlpatterns = [
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.menu, name="index"),
    path("trajets/", views.trajets, name="trajets"),
    path("reservations/", views.reservations, name="reservations"),
    path("reservations/<int:reservation_id>/", views.reservation, name="reservation"),
    path("nouvelle_reservation/", views.edit_reservation, name="nouvelle_reservation"),
    path("modifier_reservation/<int:reservation_id>/", views.edit_reservation, name="modifier_reservation"),
    path("supprimer_reservation/<int:reservation_id>/", views.delete_reservation, name="supprimer_reservation"),
]