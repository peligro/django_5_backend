from django.urls import path
from .views import *

urlpatterns = [
	path('contacto', Clase1.as_view()),
]