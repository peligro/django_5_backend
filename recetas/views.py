from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from .serializers import *
from .models import *
from django.utils.dateformat import DateFormat
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado

from jose import jwt
from django.conf import settings


# Create your views here.
class Clase1(APIView):
    
    
    def get(self, request):
        data = Receta.objects.order_by('-id').all()
        datos_json= RecetaSerializer(data, many=True)
        return JsonResponse({"data":datos_json.data})
    
    
    @logueado()
    def post(self, request):
        if request.data.get("nombre")==None or not request.data["nombre"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo")==None or not request.data["tiempo"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion")==None or not request.data["descripcion"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo descripcion es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id")==None or not request.data["categoria_id"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        
        #validamos que no exista la categoria_id
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"La categoria_id informada no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        
        
        #select * from recetas where nombre=request.data.get("nombre")
        #validamos que el nombre de la receta esté disponible
        if Receta.objects.filter(nombre=request.data.get("nombre")).exists():
            return JsonResponse({"estado":"error", "mensaje":f"El nombre {request.data["nombre"]} no está disponible"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Debe adjuntar una foto en el campo foto"}, status=HTTPStatus.BAD_REQUEST)
        
        
        #print(request.FILES["foto"].content_type)
        if request.FILES["foto"].content_type=="image/jpeg" or request.FILES["foto"].content_type=="image/png":
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url( request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":"Se produjo un error al intentar subir el archivo"}, status=HTTPStatus.BAD_REQUEST)
            
            header = request.headers.get('Authorization').split(" ")
            resuelto=jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'] )
            try:
                Receta.objects.create(nombre=request.data["nombre"], tiempo=request.data.get("tiempo"), descripcion=request.data["descripcion"], categoria_id=request.data.get("categoria_id"), fecha=datetime.now(), foto=foto, user_id=resuelto["id"])
                return JsonResponse({"estado":"ok", "mensaje":"Se crea el registro exitosamente"}, status=HTTPStatus.CREATED)
            except Exception as e:
                raise Http404
        return JsonResponse({"estado":"erro", "mensaje":"La foto sólo puede ser PNG y JPG"}, status=HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    
    
    def get(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
            return JsonResponse({"data":{"id": data.id, "nombre":data.nombre, "slug":data.slug, "tiempo":data.tiempo, "descripcion":data.descripcion, "fecha":DateFormat(data.fecha).format('d/m/Y'), "categoria_id":data.categoria_id, "categoria":data.categoria.nombre, "imagen":f"{os.getenv("BASE_URL")}uploads/recetas/{data.foto}", "user_id":data.user_id, "user":data.user.first_name}}, status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
        
    
    @logueado()
    def put(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
        except Receta.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
        
        
        if request.data.get("nombre")==None or not request.data["nombre"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo")==None or not request.data["tiempo"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion")==None or not request.data["descripcion"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo descripcion es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id")==None or not request.data["categoria_id"]:
            return JsonResponse({"estado":"error", "mensaje":"El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        #validamos que no exista la categoria_id
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"La categoria_id informada no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        
        #validamos que no exista la categoria_id
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"La categoria_id informada no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        
        
        
        try:
            Receta.objects.filter(pk=id).update(nombre=request.data["nombre"], slug=slugify(request.data["nombre"]),tiempo=request.data.get("tiempo"), descripcion=request.data["descripcion"], categoria_id=request.data.get("categoria_id"))
            return JsonResponse({"estado":"ok", "mensaje":"Se modifica el registro exitosamente"}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"}, status=HTTPStatus.NOT_FOUND)
        
    
    @logueado()  
    def delete(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
        except Receta.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
        #borrar la foto de la carpeta
        os.remove(f"./uploads/recetas/{data.foto}")
        #borrar el registro de la bd
        Receta.objects.filter(id=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se elimina el registro exitosamente"}, status=HTTPStatus.OK)
        