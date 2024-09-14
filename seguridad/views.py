from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404, HttpResponseRedirect
from http import HTTPStatus
from django.contrib.auth.models import User
import uuid
import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta
import time


from .models import *
from utilidades import utilidades


# Create your views here.

class Clase1(APIView):
    
    def post(self, request):
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("correo")==None or not request.data.get("correo"):
            return JsonResponse({"estado":"error", "mensaje":"El correo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password")==None or not request.data.get("password"):
            return JsonResponse({"estado":"error", "mensaje":"El campo password es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        
        if User.objects.filter(email=request.data["correo"]).exists():
            return JsonResponse({"estado":"error", "mensaje":f"El correo {request.data["correo"]} no está disponible"}, status=HTTPStatus.BAD_REQUEST)
        
        
        token = uuid.uuid4()
        url = f"{os.getenv("BASE_URL")}api/v1/seguridad/verificacion/{token}"
        try:
            u=User.objects.create_user(username=request.data["correo"], password=request.data["password"], email=request.data["correo"], first_name=request.data["nombre"], last_name="", is_active=0)
            UsersMetadata.objects.create(token=token, user_id=u.id)
            
            html=f""" 
            <h3>Verificación de cuenta</h3>
            Hola {request.data["nombre"]} te haz registrado exitosamente. Para activar tu cuenta haz clic en el siguiente enlace:<br/>
            <a href="{url}">{url}</a>
            <br/>
            o copia y pega la siguiente URL en tu navegador favorito:
            <br/>
            {url}
            """
            utilidades.sendMail(html, "Verificación", request.data["correo"])
            
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse({"estado":"ok", "mensaje":"Se crea el registro exitosamente"}, status=HTTPStatus.CREATED)


class Clase2(APIView):
    
    
    def get(self, request, token):
        if token==None or not token:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=404)
        
        
        try:
            data=UsersMetadata.objects.filter(token=token).filter(user__is_active=0).get()
            
            UsersMetadata.objects.filter(token=token).update(token="")
            
            User.objects.filter(id=data.user_id).update(is_active=1)
            
            return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))
        except UsersMetadata.DoesNotExist:
            raise Http404


class Clase3(APIView):
    
    
    def post(self, request):
        
        if request.data.get("correo")==None or not request.data.get("correo"):
            return JsonResponse({"estado":"error", "mensaje":"El correo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password")==None or not request.data.get("password"):
            return JsonResponse({"estado":"error", "mensaje":"El campo password es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        
        #select * from auth_user where correo=correo
        try:
            user = User.objects.filter(email=request.data["correo"]).get()
        except User.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
        
        
        auth = authenticate(request, username=request.data.get("correo"), password=request.data.get("password") )
        if auth is not None:
            fecha = datetime.now()
            despues = fecha + timedelta(days=1)
            fecha_numero = int(datetime.timestamp(despues))
            payload={"id":user.id, "ISS":os.getenv("BASE_URL"), "iat":int(time.time()), "exp":int(fecha_numero)}
            try:
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id":user.id, "nombre":user.first_name, "token":token})
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":"Ocurió un error inesperado"}, status=HTTPStatus.BAD_REQUEST) 
        else:
            return JsonResponse({"estado":"error", "mensaje":"Las credenciales ingresadas no son correctas"}, status=HTTPStatus.BAD_REQUEST)
            
            
        