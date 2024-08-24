from rest_framework import serializers
import os
from dotenv import load_dotenv
from .models import *


class RecetaSerializer(serializers.ModelSerializer):
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    #categoria = serializers.CharField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.first_name')


    class Meta:
        model = Receta
        fields=("id", "nombre", "slug", "tiempo", "descripcion", "fecha", "categoria_id", "categoria", "imagen", "user_id", "user")
        #fields = '__all__'
        #fields=('__all__')
    
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/recetas/{obj.foto}" 