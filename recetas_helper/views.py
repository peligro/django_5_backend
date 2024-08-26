from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404
from http import HTTPStatus
from recetas.models import *
from categorias.models import *
from django.contrib.auth.models import User
from recetas.serializers import *
from categorias.models import *
from categorias.models import *
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from seguridad.decorators import logueado
from utilidades import utilidades

class Clase1(APIView):
    
    
    def post(self, request):
        
        if request.data.get("id")==None or not request.data.get("id"):
            return JsonResponse({"estado":"error", "mensaje":"El campo id es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        #validaciones si existe o no la categoría
        try:
            existe = Receta.objects.filter(pk=request.data['id']).get()
            anterior=existe.foto
        except Receta.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":f"La receta informada no existe en la base de datos"},  status=HTTPStatus.BAD_REQUEST)
        
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
                Receta.objects.filter(id = request.data['id']).update(foto = foto)
                os.remove(f"./uploads/recetas/{anterior}")
                return JsonResponse({"estado":"ok", "mensaje":"Se modificó el registro exitosamente"},  status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"estado":"error", "mensaje":f"La foto sólo puede ser PNG o JPG"},  status=HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    
    def get(self, request, slug):
        try:
            data = Receta.objects.filter(slug=slug).get()
            return JsonResponse({"data":{"id":data.id, "nombre":data.nombre, "slug":data.slug, "tiempo":data.tiempo, "descripcion":data.descripcion, "fecha":DateFormat(data.fecha).format('d/m/Y'), "categoria_id":data.categoria_id, "categoria":data.categoria.nombre, "imagen":f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}", "user_id":data.user_id, "user":data.user.first_name}}    ,  status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            raise Http404


class Clase3(APIView):
    
    def get(self, request):
        data=Receta.objects.order_by('?').all()[:3]
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)


class Clase4(APIView):
    
    
    @logueado()
    def get(self, request, id):
        try:
            existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":f"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        data=Receta.objects.filter(user_id=id).all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)


class Clase5(APIView):
    
    def get(self, request):
        if request.GET.get('categoria_id')==None or not request.GET.get('categoria_id'):
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado 1"},  status=HTTPStatus.BAD_REQUEST)
        try:
            existe = Categoria.objects.filter(pk=request.GET.get('categoria_id')).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":f"Ocurrió un error inesperado 3"},  status=HTTPStatus.BAD_REQUEST)
        data=Receta.objects.filter(categoria_id=request.GET.get('categoria_id')).filter(nombre__icontains=request.GET.get('search')).all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)
    

class Clase6(APIView):
    
    def get(self, request):
        data=Receta.objects.order_by('-id').all()
        paginar=utilidades.paginacion(data, request)
        print(paginar)
        datos_json = RecetaSerializer(paginar[0], many=True)
        
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)

