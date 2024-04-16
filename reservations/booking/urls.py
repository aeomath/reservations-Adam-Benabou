from django.urls import path,include

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name="index"),
    path("trajets/", views.trajets, name="trajets"),
    path("reservations/", views.reservations, name="reservations"),
]