from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import *
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from recetas.models import *

# Create your views here.

class Clase1(APIView):
    
    
    def get(self, request):
        #select * from categorias order by id desc;
        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many=True)
        #return Response(datos_json.data)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)
    
    
    def post(self, request):
        if request.data.get("nombre")==None or not request.data['nombre']:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Categoria.objects.create(nombre=request.data['nombre'])
            return JsonResponse({"estado":"ok", "mensaje":"Se crea el registro exitosamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404


class Clase2(APIView):
    
    
    def get(self, request, id):
        #select * from categorias where id=4;
        try:
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({"data": {"id":data.id, "nombre":data.nombre, "slug":data.slug}}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
    
    
    def put(self, request, id):
        if request.data.get("nombre")==None:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(pk=id).update(nombre=request.data.get("nombre"), slug=slugify(request.data.get("nombre")))
            return JsonResponse({"estado":"ok", "mensaje":"Se modifica el registro exitosamente"}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
        
        
    def delete(self, request, id):
        try:
            data = Categoria.objects.filter(pk=id).get()
           
        except Categoria.DoesNotExist:
            raise Http404
        
        if Receta.objects.filter(categoria_id=id).exists():
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        
        Categoria.objects.filter(pk=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se elimina el registro exitosamente"}, status=HTTPStatus.OK)