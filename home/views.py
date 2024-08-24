from django.shortcuts import render
from django.http import HttpResponse

def home_inicio(request):
	return HttpResponse("<h1>Hola mundo desde Python 3.12 y Django 5</h1>")