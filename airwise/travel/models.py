from django.db import models

class Utilisateur(models.Model):
    ROLES = [
        ("voyageur", "Voyageur"),
        ("compagnie", "Compagnie"),
    ]

    nomComplet = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES, default="voyageur")

    def __str__(self):
        return f"{self.nomComplet} ({self.email})"


# --- TRAVEL COMPANIES ---
class CompagnieVoyage(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=[("Avion", "Avion"), ("Bus", "Bus"), ("Train", "Train"), ("Tour", "Tourisme")]
    )

    def __str__(self):
        return self.nom


# --- DESTINATIONS ---
class Destination(models.Model):
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    pays_depart = models.CharField(max_length=100)
    pays_arrivee = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee}"


# --- FLIGHTS / ROUTES ---
class Trajet(models.Model):
    compagnie = models.ForeignKey(CompagnieVoyage, on_delete=models.CASCADE, related_name="trajets")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="trajets")
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.compagnie.nom} | {self.destination}"


# --- WEATHER CONDITIONS ---
class Meteo(models.Model):
    ville = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    conditions = models.CharField(max_length=100)
    humidite = models.FloatField()
    vent = models.FloatField()

    def __str__(self):
        return f"{self.ville} - {self.date}"


# --- PRICE PREDICTIONS ---
class PredictionPrix(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="predictions")
    date_prediction = models.DateTimeField(auto_now_add=True)
    prix_estime = models.DecimalField(max_digits=10, decimal_places=2)
    saison = models.CharField(max_length=50)
    meteo = models.ForeignKey(Meteo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Price Prediction {self.trajet} : {self.prix_estime} EUR"


# --- RESERVATIONS ---
class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="reservations")
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="reservations", null=True, blank=True)
    flight_id = models.CharField(max_length=100, blank=True, default='')
    origin = models.CharField(max_length=100, blank=True, default='')
    destination = models.CharField(max_length=100, blank=True, default='')
    departure_date = models.CharField(max_length=20, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_reservation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=50,
        choices=[("Confirmed", "Confirmed"), ("Pending", "Pending"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"Reservation {self.utilisateur} - {self.origin} to {self.destination}"

