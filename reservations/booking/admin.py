from django.contrib import admin
from .models import Gare, Trajet



class TrajetAdmin(admin.ModelAdmin):
    list_display = ('__str__','date_depart', 'date_arrivee')
    list_filter = ('gare_depart', 'gare_arrivee')
    search_fields = ('gare_depart', 'gare_arrivee')
    fieldsets = (
        (None, { 'fields': ['gare_depart', 'gare_arrivee']}),
        ("Date information", {'fields': ['date_depart','date_arrivee']}),
        
    )
    
class GareAdmin(admin.ModelAdmin):
    list_filter = ('ville',)
    search_fields = ('nom', 'ville')
    list_display = ('nom', 'ville')
# Register your models here.
admin.site.register(Gare, GareAdmin)
admin.site.register(Trajet, TrajetAdmin)