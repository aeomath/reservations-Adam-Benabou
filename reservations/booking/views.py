from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Trajet,Reservation,Passager
from booking.form import SearchForm , ReservationForm, Register_Client,PassagerForm, ItineraryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from .models import Trajet

import json

    
def menu(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'booking/menu_auth.html', context)
    return render(request, 'booking/menu_pas_auth.html')

import networkx as nx
import math



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

@login_required()
def profil(request):
    template = "booking/profil.html"
    passager = Passager.objects.filter(client=request.user.client)
    return render(request, template, {'passagers': passager})

@login_required()
def create_passager(request):
    if request.method == 'POST':
        form = PassagerForm(request.POST)
        if form.is_valid():
            passager = form.save(commit=False)
            passager.client = request.user.client
            passager.save()
            return redirect('profil')
    else:
        form = PassagerForm()
    return render(request, 'booking/create_passager.html', {'form': form})

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

@login_required()
def reservations(request):
    ## si un utlisateur n'est pas encore client , alors il n'a pas de réservation
    ## normalement , ca n'arrive pas car lorsque l'utilisateur s'inscrit , il s'inscrit en tant que client ( sauf les admins qui ne sont pas clients )
    if hasattr(request.user, 'client'):
        reservations_list = Reservation.objects.filter(client=request.user.client)
    else :
        reservations_list = []
    template = "booking/reservations.html"
    return render(request, template, {'reservations': reservations_list})

@login_required()
def reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.client != request.user.client:
        return HttpResponse("Petit malin , vous avez essayé d'accéder à une réservation qui ne vous appartient pas !")
    template = "booking/reservation.html"
    depart_time = reservation.trajet.date_depart.isoformat()
    context ={'reservation': reservation, 
              'trajet': reservation.trajet , 
              'gare_depart': reservation.trajet.gare_depart, 
              'gare_arrivee': reservation.trajet.gare_arrivee , 
              'depart_time': depart_time} 
    return render(request, template, context=context)

@login_required()
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

@login_required()
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if reservation.client != request.user.client:
        return HttpResponse("Petit malin , vous avez essayé de supprimer une réservation qui ne vous appartient pas !")
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations')
    template = "booking/delete_reservation.html"
    return render(request, template, {'reservation': reservation})

# def column_chart_view(request, chart_info):
#     return render(request, 'booking/chart.html', {'chart_info': chart_info})

def chart_reservations_par_trajet_par_jour(request, date):
    chart_info = {
        'type': 'column',
        'title': "Sample Title",
        'y_axis_label' : "Nombre de réservations",
        'data' : [
            ['Corn', [406292, 260000, 107000, 68300, 27500, 14500]],
            ['Wheat', [51086, 136000, 5500, 141000, 107180, 77000]]
        ]
    }
    
    trajets = get_list_or_404(Trajet)
    
    dictio = {"trajet_name": []} ## {date: [nb_res_par_trajet]}
    
    for trajet in trajets:
        res_by_day = Trajet.nb_reservations_par_jour(trajet)
        dictio.update({key: dictio[key].append[res_by_day[key]] if key in res_by_day else dictio[key] for key in dictio})
        dictio.update({key: res_by_day[key] for key in res_by_day if key not in dictio})
        
        
    chart_info['categories'] = dictio.keys()
        
        
    return render(request, 'booking/chart.html', {'chart_info': chart_info})
def chart_remplissage(request, id):
    trajet = Trajet.objects.get(pk=id)
    toPlot = trajet.nb_reservations_chaque_jour()
    chart_info = {
        'type': 'line',
        'title': "Taux de remplissage du trajet " + str(trajet),
        'x_label': "Date",
        'y_axis_label': "Taux de remplissage",
        'data': toPlot
    }
    template = "/booking/chart"
    return render(request, template, {"chart_info":chart_info})

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

@login_required()
def profil(request):
    template = "booking/profil.html"
    return render(request, template)






@login_required()
def itineraire(request):
    template = "booking/itinerary.html"
    
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['gare_depart']
            target = form.cleaned_data['gare_arrivee']
            start_datetime = form.cleaned_data['date_de_depart']   
            
            itinerary_list = compute_itinerary(source, target, start_datetime)
        else:
            itinerary_list = get_list_or_404(Trajet)
    else:
        itinerary_list = get_list_or_404(Trajet)
        form = ItineraryForm()
    context = {
        'form': form,
        'itineraire': itinerary_list,
    }
    return render(request, template, context)
       


def compute_itinerary(source, target, start_datetime):    
    #Create Graph
    graph = create_graph(start_datetime)
    #Compute te shortest path from A to B
    shortest_path = nx.bellman_ford_path(graph, source, target, weight='weight')
    #Create the itinerary
    itinerary = []
    for i in range(len(shortest_path)-1):
        itinerary.append(get_object_or_404(Trajet, gare_depart = shortest_path[i], gare_arrivee = shortest_path[i+1]))
    return itinerary
    
def create_graph(start_datetime):
    G = nx.Graph()
    trajet_liste = get_list_or_404(Trajet)
    for trajet in trajet_liste:
        if trajet.date_depart >= start_datetime:
            list_edge = compute_edge(trajet)
            G.add_edge(list_edge[0],list_edge[1], weight=list_edge[2])
    return G

def compute_edge(trajet):
    A = trajet.gare_depart
    B = trajet.gare_arrivee
    return [trajet.gare_depart, trajet.gare_arrivee, calculate_distance(A.position.latitude ,A.position.longitude,
                                                                        B.position.latitude, B.position.longitude)]
    
    
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
    
def nouvel_itineraire(request, trajet_id):
    
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
            
    template = "booking/reservation_itineraire.html"
    return render(request, template, {'form': form})
