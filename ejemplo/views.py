from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
#from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
#upload
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime


# Create your views here.
class Class_Ejemplo(APIView):
    
    
    def get(self, request):
        #return HttpResponse(f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug')}")
        #return Response({"estado":"ok", "mensaje":f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug')}"})
        return JsonResponse({"estado":"ok", "mensaje":f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug')}"}, status=HTTPStatus.OK)
    
    
    def post(self, request):
        if request.data.get("correo")==None or request.data.get("password")==None:
            raise Http404
        #return HttpResponse("Método POST")
        return JsonResponse({"estado":"ok", "mensaje":f"Método POST | correo={request.data.get('correo')} | password={request.data.get('password')}"}, status=HTTPStatus.CREATED)
    

class Class_EjemploParametros(APIView):
    
    
    def get(self, request, id):
        return HttpResponse(f"Método GET | parámetro={id}")
    
    
    def put(self, request, id):
        return HttpResponse(f"Método PUT | parámetro={id}")
    
    
    def delete(self, request, id):
        return HttpResponse(f"Método DELETE | parámetro={id}")


class Class_EjemploUpload(APIView):
    
    
    def post(self, request):
        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file']))[1]}"
        fs.save(f"ejemplo/{foto}", request.FILES['file'])
        fs.url( request.FILES['file'])
        return JsonResponse({"estado":"ok", "mensaje":"Se subió el archivo"})
    