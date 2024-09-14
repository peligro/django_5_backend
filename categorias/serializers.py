from rest_framework import serializers
from .models import *


class CategoriaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categoria
        #fields = ("id", "nombre", "slug")
        fields = '__all__'
        #fields= ('__all__')