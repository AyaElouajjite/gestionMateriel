from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Materiel, Categorie, Emprunt
from django.utils import timezone
from django.http import HttpResponseForbidden

def is_admin(user):
    return user.is_superuser

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie!')
            return redirect('materiel:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'materiel/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('materiel:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'materiel/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('materiel:login')

@login_required
def dashboard(request):
    categorie_id = request.GET.get('categorie')
    categories = Categorie.objects.all()
    
    if categorie_id:
        materiels = Materiel.objects.filter(categorie_id=categorie_id)
    else:
        materiels = Materiel.objects.all()
    
    emprunts_actifs = Emprunt.objects.filter(
        utilisateur=request.user,
        date_retour_effective__isnull=True
    )
    
    context = {
        'materiels': materiels,
        'categories': categories,
        'emprunts_actifs': emprunts_actifs,
        'is_admin': request.user.is_superuser,
        'categorie_selectionnee': int(categorie_id) if categorie_id else None,
    }
    return render(request, 'materiel/dashboard.html', context)

@login_required
def emprunter_materiel(request, materiel_id):
    if request.method == 'POST':
        materiel = get_object_or_404(Materiel, id=materiel_id)
        if materiel.etat == 'disponible':
            emprunt = Emprunt.objects.create(
                utilisateur=request.user,
                materiel=materiel,
                date_emprunt=timezone.now(),
                date_retour_prevue=timezone.now() + timezone.timedelta(days=7)
            )
            materiel.etat = 'emprunte'
            materiel.save()
            messages.success(request, f'Vous avez emprunté {materiel.nom}')
        else:
            messages.error(request, 'Ce matériel n\'est pas disponible')
    return redirect('materiel:dashboard')

@login_required
@user_passes_test(is_admin)
def gestion_materiel(request):
    materiels = Materiel.objects.all()
    categories = Categorie.objects.all()
    context = {
        'materiels': materiels,
        'categories': categories,
    }
    return render(request, 'materiel/gestion_materiel.html', context)

@login_required
def retourner_materiel(request, emprunt_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas les droits pour effectuer cette action.")
        
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    if request.method == 'POST':
        emprunt.date_retour_effective = timezone.now()
        emprunt.save()
        
        materiel = emprunt.materiel
        materiel.etat = 'disponible'
        materiel.save()
        
        messages.success(request, f'Le matériel {materiel.nom} a été retourné avec succès')
    return redirect('materiel:dashboard')
