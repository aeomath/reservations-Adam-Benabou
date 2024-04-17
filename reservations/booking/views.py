from django.shortcuts import get_list_or_404, get_object_or_404, render,redirect
from django.http import HttpResponse
from .models import Trajet,Gare,Client,Passager,Reservation
from booking.form import SearchForm , PassagerForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Trajet

@login_required(login_url='/booking/accounts/login')
def trajets(request):
    template = "booking/trajets.html"
    trajets = Trajet.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_dep = form.cleaned_data['gare_depart']
            search_arr = form.cleaned_data['gare_arrivee']
            if search_dep:
                trajets = trajets.filter(gare_depart__nom=search_dep)
            if search_arr:
                trajets = trajets.filter(gare_arrivee__nom=search_arr)
        else:
            trajets = get_list_or_404(Trajet)
    else:
        trajets = get_list_or_404(Trajet)
        form = SearchForm()

    context = {
        'form': form,
        'trajets': trajets,
    }

    return render(request, template, context)

@login_required(login_url='/booking/accounts/login')
def reservations(request):
    ## si un utlisateur n'est pas encore client , alors il n'a pas de réservation
    ## normalement , ca n'arrive pas car lorsque l'utilisateur s'inscrit , il s'inscrit en tant que client ( sauf les admins qui ne sont pas clients )
    if hasattr(request.user, 'client'):
        reservations_list = Reservation.objects.filter(client=request.user.client)
    else :
        reservations_list = []
    template = "booking/reservations.html"
    return render(request, template, {'reservations': reservations_list})

@login_required(login_url='/booking/accounts/login')
def reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.client != request.user.client:
        return HttpResponse("Petit malin , vous avez essayé d'accéder à une réservation qui ne vous appartient pas !")
    template = "booking/reservation.html"
    return render(request, template, {'reservation': reservation})

## saisie d'une réservation
@login_required(login_url='/booking/accounts/login')
def edit_reservation(request):
    if request.method == 'GET':
        form = ReservationForm()
        passager_form = PassagerForm()
    elif request.method == 'POST':
        form = ReservationForm(request.POST)
        passager_form = PassagerForm(request.POST)
        if form.is_valid() and passager_form.is_valid():
            ## n'enregistre pas encore la réservation
            reservation=form.save(commit=False)
            reservation.client = request.user.client
            reservation.passager = passager_form.save()
            reservation.date_reservation = timezone.now()    
            ## enregistre la réservation
            reservation.save()
            return redirect('reservations')
    template = "booking/edit_reservation.html"
    return render(request, template, {'form': form , 'passager_form': passager_form})

def index(request):
    return HttpResponse("Hello, world. You're at the booking index.")


