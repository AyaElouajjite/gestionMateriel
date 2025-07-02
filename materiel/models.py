from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

class Materiel(models.Model):
    ETAT_CHOICES = [
        ('disponible', 'Disponible'),
        ('emprunte', 'Emprunté'),
        ('maintenance', 'En maintenance'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField()
    numero_serie = models.CharField(max_length=100, unique=True)
    date_acquisition = models.DateField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible')
    image = models.ImageField(upload_to='materiel_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.numero_serie})"

    class Meta:
        verbose_name = "Matériel"
        verbose_name_plural = "Matériels"

class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour_prevue = models.DateTimeField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"Emprunt de {self.materiel.nom} par {self.utilisateur.username}"

    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
