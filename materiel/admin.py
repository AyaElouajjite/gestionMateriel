from django.contrib import admin
from .models import Categorie, Materiel, Emprunt
from django.utils import timezone

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('nom', 'numero_serie', 'categorie', 'etat', 'date_acquisition')
    list_filter = ('categorie', 'etat')
    search_fields = ('nom', 'numero_serie', 'description')
    date_hierarchy = 'date_acquisition'
    ordering = ('-date_acquisition',)
    list_editable = ('etat',)
    list_per_page = 20

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('materiel', 'utilisateur', 'date_emprunt', 'date_retour_prevue', 'date_retour_effective', 'statut_emprunt')
    list_filter = ('date_emprunt', 'date_retour_effective', 'utilisateur')
    search_fields = ('utilisateur__username', 'materiel__nom')
    date_hierarchy = 'date_emprunt'
    ordering = ('-date_emprunt',)
    list_per_page = 20

    def statut_emprunt(self, obj):
        if obj.date_retour_effective:
            return 'Retourné'
        elif obj.date_retour_prevue < timezone.now():
            return 'En retard'
        else:
            return 'En cours'
    statut_emprunt.short_description = 'Statut'
