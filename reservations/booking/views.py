from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Trajet,Reservation
from booking.form import SearchForm , ReservationForm, Register_Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone



from .models import Trajet


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

@login_required(login_url='/booking/accounts/login')
def edit_reservation(request, reservation_id=None,trajet_id=None):     
    ##Modification d'une réservation existante   
    if reservation_id:
        if request.user.client != get_object_or_404(Reservation, pk=reservation_id).client:
            return HttpResponse("Petit malin , vous avez essayé de modifier une réservation qui ne vous appartient pas !")
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        if request.method == 'POST':
            form = ReservationForm(data = request.POST, instance=reservation)
            if form.is_valid():
                reservation = form.save()
                return redirect('reservation',reservation_id=reservation.pk)
        else:
            form = ReservationForm(instance=reservation)
        template = "booking/edit_reservation.html"
        return render(request, template, {'form': form, 'reservation_id': reservation_id})
    
    ##Création d'une nouvelle réservation
    else:
        if request.method == 'POST':
            form = ReservationForm(data = request.POST,client = request.user.client)
            if form.is_valid():
                reservation = form.save(commit=False)
                ## Si on choisit un trajet à reserver , et donc si un trajet est en paramètre, on l'ajoute à la réservation
                if trajet_id:
                    reservation.trajet = get_object_or_404(Trajet, pk=trajet_id)
                reservation.client = request.user.client
                reservation.date_reservation = timezone.now()   
                reservation.save()
                form.save_m2m()
                return redirect('reservation',reservation_id=reservation.pk)
        else:
            if trajet_id:
                trajet = get_object_or_404(Trajet, pk=trajet_id)
                reservation=Reservation(trajet=trajet)
                form = ReservationForm(instance=reservation,client = request.user.client)
            ## Si on ne choisit pas de trajet à reserver , on crée une réservation vide
            else:
                form = ReservationForm(client = request.user.client)
                
    template = "booking/edit_reservation.html"
    return render(request, template, {'form': form})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.client != request.user.client:
        return HttpResponse("Petit malin , vous avez essayé de supprimer une réservation qui ne vous appartient pas !")
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations')
    template = "booking/delete_reservation.html"
    return render(request, template, {'reservation': reservation})
    
def menu(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'booking/menu_auth.html', context)
    return render(request, 'booking/menu_pas_auth.html')

def register(request):
    if request.method == 'POST':
        form = Register_Client(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            prenom = form.cleaned_data['prenom']
            nom = form.cleaned_data['nom']
            new_user = User.objects.create_user(username=username, password=password, first_name=prenom, last_name=nom)
            client.user = new_user
            client.save()
            login(request, new_user)
            return redirect('menu')
    else:
        form = Register_Client()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/booking/accounts/login')
def profil(request):
    template = "booking/profil.html"
    return render(request, template)


