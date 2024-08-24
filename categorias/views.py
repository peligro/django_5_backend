from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.http import Http404
from http import HTTPStatus
from .models import *
from recetas.models import *
from .serializers import CategoriaSerializer
from django.utils.text import slugify
from seguridad.decorators import logueado



class Clase1(APIView):
    
    ###petición vía GET
    #Response pedirá un archivo llamado api.html en el navegador
    def get(self, request):
        data=Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many=True)
        #return Response(datos_json.data)
        return JsonResponse({"data":datos_json.data}, status=HTTPStatus.OK)
    
    
    
    @logueado()
    def post(self, request):
        if request.data.get("nombre")==None:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        try:
            Categoria.objects.create(nombre=request.data['nombre'])
            return JsonResponse({"estado":"ok", "mensaje":"Se creó el registro exitosamente"},  status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
    


class Clase2(APIView):
    
    
    def get(self, request, id):
        try:
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({"data":{"nombre":data.nombre, "slug":data.slug}}    ,  status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404


    @logueado()
    def put(self, request, id):
        if request.data.get("nombre")==None:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        try:
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(id = id).update(nombre = request.data.get("nombre"),  slug=slugify(request.data.get("nombre")))
            return JsonResponse({"estado":"ok", "mensaje":"Se modificó el registro exitosamente"}    ,  status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404


    @logueado()
    def delete(self, request, id):
        try:
            data = Categoria.objects.filter(id=id).get()
        except Categoria.DoesNotExist:
            raise Http404
        if Receta.objects.filter(categoria_id=id).exists():
            return JsonResponse({"estado":"error", "mensaje":f"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        Categoria.objects.filter(id=id).delete()
        return JsonResponse({"estado":"ok", "mensaje":"Se eliminó el registro exitosamente"}    ,  status=HTTPStatus.CREATED)