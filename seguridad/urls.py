from django.urls import path
from .views import *

urlpatterns = [
    path('seguridad/registro', Clase1.as_view()),
    path('seguridad/verificacion/<str:token>', Clase2.as_view()),
    path('seguridad/login', Clase3.as_view()),
]
