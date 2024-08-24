from django.urls import path
from .views import *

urlpatterns = [
	path('ejemplo', Class_Ejemplo.as_view()),
    path('ejemplo/<int:id>', Class_EjemploParametro.as_view()),
    path('ejemplo-upload', Class_EjemploUpload.as_view()),
]