from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
import os
from seguridad.decorators import logueado

class Class_Ejemplo(APIView):
    
    
    #para que no te pase error con la identación busca con F1: convert indentation to tabs
    # ###petición vía GET
    @logueado()
    def get(self, request):
        headers=request.headers.get('Authorization', None)
        return JsonResponse(  {"estado":"ok", "mensaje":f"Método GET | id={request.GET.get('id', None)}| slug={request.GET.get('slug', None)} | header={headers}"},  status=HTTPStatus.OK)
        #return Response({"estado":"ok", "mensaje":f"Método GET | id={request.GET.get('id', None)}| slug={request.GET.get('slug', None)} | header={headers}"})
        #return HttpResponse("Método GET")
        #return HttpResponse(f"Método GET | id={request.GET.get('id', None)}| slug={request.GET.get('slug', None)} | header={headers}")
    
    
    @logueado()
    def post(self, request):
        if request.data.get("correo")==None or request.data.get("password")==None:
            raise Http404
        return HttpResponse(f"Método POST | correo={request.data.get("correo")} | password={request.data.get("password")}")
    
    """
    def post(self, request):
        return HttpResponse("Método POST")
    
    
    def put(self, request):
        return HttpResponse("Método PUT")
    
    def delete(self, request):
        return HttpResponse("Método Delete")
    """

class Class_EjemploParametro(APIView):
    
    @logueado()
    def get(self, request, id):
        return HttpResponse(f"Método GET | id={id}")
    
    def put(self, request, id):
        return HttpResponse(f"Método PUT | id={id}")
    
    def delete(self, request, id):
        return HttpResponse(f"Método DELETE | id={id}")


class Class_EjemploUpload(APIView):
    
    def post(self, request):
        fs=FileSystemStorage()
        fecha=datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file']))[1]}"
        filename = request.FILES.get('file')
        fs.save(f"ejemplo/{foto}", request.FILES['file'])
        fs.url(filename)
        return JsonResponse({"estado":"ok", "mensaje":f"Se subió el archivo | dato={request.data.get("dato")} | file={foto}"})