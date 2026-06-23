from django.contrib import admin
from .models import Utilisateur, CompagnieVoyage, Destination, Trajet, Meteo, PredictionPrix, Reservation


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nomComplet', 'email', 'telephone', 'role')
    search_fields = ('nomComplet', 'email')
    list_filter = ('role',)


@admin.register(CompagnieVoyage)
class CompagnieVoyageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pays', 'ville', 'type')
    search_fields = ('nom',)
    list_filter = ('type', 'pays')


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('ville_depart', 'ville_arrivee', 'pays_depart', 'pays_arrivee')
    search_fields = ('ville_depart', 'ville_arrivee')


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ('compagnie', 'destination', 'date_depart', 'date_arrivee', 'prix')
    list_filter = ('compagnie', 'date_depart')
    search_fields = ('compagnie__nom',)


@admin.register(Meteo)
class MeteoAdmin(admin.ModelAdmin):
    list_display = ('ville', 'date', 'temperature', 'conditions')
    list_filter = ('date',)


@admin.register(PredictionPrix)
class PredictionPrixAdmin(admin.ModelAdmin):
    list_display = ('trajet', 'prix_estime', 'saison', 'date_prediction')
    list_filter = ('saison',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'origin', 'destination', 'departure_date', 'price', 'statut', 'date_reservation')
    list_filter = ('statut', 'date_reservation')
    search_fields = ('utilisateur__nomComplet', 'origin', 'destination')
