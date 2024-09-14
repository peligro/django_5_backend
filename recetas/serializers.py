from rest_framework import serializers
from .models import *
from dotenv import load_dotenv
import os


class RecetaSerializer(serializers.ModelSerializer):
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    #categoria = serializers.CharField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")#13/10/2025
    imagen = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.first_name')
    
    
    class Meta:
        model = Receta
        fields = ("id", "nombre", "slug", "tiempo", "descripcion", "fecha", "categoria", "categoria_id", "imagen", "user_id", "user")
        
    
    def get_imagen(self, obj):
        return f"{os.getenv("BASE_URL")}uploads/recetas/{obj.foto}"