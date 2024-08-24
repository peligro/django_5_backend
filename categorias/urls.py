from django.urls import path
from .views import *

urlpatterns = [
	path('categorias', Clase1.as_view()),
    path('categorias/<int:id>', Clase2.as_view()),
]