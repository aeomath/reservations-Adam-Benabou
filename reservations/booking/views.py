from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse
from .models import Trajet, Gare
from booking.form import SearchForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render

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

def index(request):
    return HttpResponse("Hello, world. You're at the booking index.")


