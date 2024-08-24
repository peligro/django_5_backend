from django.urls import path
from .views import *

urlpatterns = [
	path('recetas/editar/foto', Clase1.as_view()),
    path('recetas/slug/<str:slug>', Clase2.as_view()),
    path('recetas-home', Clase3.as_view()),
    path('recetas-panel/<int:id>', Clase4.as_view()),
    path('recetas-buscador', Clase5.as_view())
]