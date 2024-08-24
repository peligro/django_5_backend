from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.http import Http404
from http import HTTPStatus
from .models import *
from categorias.models import *
from .serializers import *
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.core.paginator import Paginator
from seguridad.decorators import logueado


class Clase1(APIView):
    
    
    def get(self, request):
        data=Receta.objects.order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        #return Response(datos_json.data)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)
    
    
    @logueado()
    def post(self, request):
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo")==None or not request.data.get("tiempo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo tiempo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion")==None or not request.data.get("descripcion"):
            return JsonResponse({"estado":"error", "mensaje":"El campo descripcion es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id")==None or not request.data.get("categoria_id"):
            return JsonResponse({"estado":"error", "mensaje":"El campo categoria_id es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        
    
        #validaciones si existe o no la receta
        if Receta.objects.filter(nombre=request.data['nombre']).exists():
            return JsonResponse({"estado":"error", "mensaje":f"El nombre {request.data['nombre']} no está disponible"},  status=HTTPStatus.BAD_REQUEST)
        
        #validaciones si existe o no la categoría
        try:
            categoria = Categoria.objects.filter(pk=request.data['categoria_id']).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":f"La categoría informada no existe en la base de datos"},  status=HTTPStatus.BAD_REQUEST)
        
        fs=FileSystemStorage()
        #validaciones para foto
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as m:
            return JsonResponse({"estado":"error", "mensaje":f"Debe adjuntar una foto para la receta"},  status=HTTPStatus.BAD_REQUEST)
        if request.FILES['foto'].content_type=="image/jpeg" or request.FILES['foto'].content_type=="image/png": 
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as a:
                return JsonResponse({"estado":"error", "mensaje":f"No se pudo subir la foto"},  status=HTTPStatus.BAD_REQUEST)
            try:
                Receta.objects.create(nombre=request.data['nombre'], tiempo=request.data['tiempo'], descripcion=request.data['descripcion'], categoria_id=request.data['categoria_id'], foto=foto, fecha=datetime.now())
                return JsonResponse({"estado":"ok", "mensaje":"Se creó el registro exitosamente"},  status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"estado":"error", "mensaje":f"La foto sólo puede ser PNG o JPG"},  status=HTTPStatus.BAD_REQUEST)
        
        
        """ 
        def post(self, request):
        print(request.data.get("nombre"))
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo")==None or not request.data.get("tiempo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo tiempo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion")==None or not request.data.get("descripcion"):
            return JsonResponse({"estado":"error", "mensaje":"El campo descripcion es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id")==None or not request.data.get("categoria_id"):
            return JsonResponse({"estado":"error", "mensaje":"El campo categoria_id es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if Receta.objects.filter(nombre=request.data['nombre']).exists():
            return JsonResponse({"estado":"error", "mensaje":f"El nombre {request.data['nombre']} no está disponible"},  status=HTTPStatus.BAD_REQUEST)
        try:
            Receta.objects.create(nombre=request.data['nombre'], tiempo=request.data['tiempo'], descripcion=request.data['descripcion'], categoria_id=request.data['categoria_id'], foto="sss", fecha=datetime.now())
            return JsonResponse({"estado":"ok", "mensaje":"Se creó el registro exitosamente"},  status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
        """


class Clase2(APIView):
    
    
    
    def get(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
            return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug, "tiempo":data.tiempo, "descripcion":data.descripcion, "fecha":DateFormat(data.fecha).format('d/m/Y'), "categoria_id":data.categoria_id, "categoria":data.categoria.nombre, "imagen":f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}", "user_id":data.user_id, "user":data.user.first_name}}    ,  status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            raise Http404
    
    
    @logueado()
    def put(self, request, id):
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo")==None or not request.data.get("tiempo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo tiempo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion")==None or not request.data.get("descripcion"):
            return JsonResponse({"estado":"error", "mensaje":"El campo descripcion es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id")==None or not request.data.get("categoria_id"):
            return JsonResponse({"estado":"error", "mensaje":"El campo categoria_id es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        #validaciones si existe o no la categoría
        try:
            categoria = Categoria.objects.filter(pk=request.data['categoria_id']).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":f"La categoría informada no existe en la base de datos"},  status=HTTPStatus.BAD_REQUEST)
        try:
            data = Receta.objects.filter(pk=id).get()
            Receta.objects.filter(id = id).update(nombre = request.data.get("nombre"),  slug=slugify(request.data.get("nombre")), tiempo=request.data.get("tiempo"), descripcion=request.data.get("descripcion"), categoria_id=request.data.get("categoria_id"))
            return JsonResponse({"estado":"ok", "mensaje":"Se modificó el registro exitosamente"}    ,  status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            raise Http404
    
    
    
    @logueado()
    def delete(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
        except Receta.DoesNotExist:
            raise Http404
        os.remove(f"./uploads/recetas/{data.foto}")
        Receta.objects.filter(id=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se eliminó el registro exitosamente"}    ,  status=HTTPStatus.CREATED)