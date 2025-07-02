from django.urls import path
from . import views

app_name = 'materiel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('emprunter/<int:materiel_id>/', views.emprunter_materiel, name='emprunter_materiel'),
    path('gestion/', views.gestion_materiel, name='gestion_materiel'),
    path('retourner/<int:emprunt_id>/', views.retourner_materiel, name='retourner_materiel'),
] 