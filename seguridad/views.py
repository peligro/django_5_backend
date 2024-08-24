from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.http import Http404, HttpResponseRedirect
from http import HTTPStatus
from .models import *
from django.contrib.auth.models import User
from categorias.models import *
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.core.paginator import Paginator
import uuid
from utilidades import utilidades
from django.contrib.auth import authenticate
from django.conf import settings
from jose import jwt

class Clase1(APIView):
    
    
    def post(self, request):
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("correo")==None or not request.data.get("correo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo correo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password")==None or not request.data.get("password"):
            return JsonResponse({"estado":"error", "mensaje":"El campo password es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        
        #validaciones si existe o no el correo
        if User.objects.filter(email=request.data['correo']).exists():
            return JsonResponse({"estado":"error", "mensaje":f"El correo {request.data['nombre']} no está disponible"},  status=HTTPStatus.BAD_REQUEST)
        token=uuid.uuid4()
        url=f"{os.getenv('BASE_URL')}api/v1/seguridad/verificacion/{token}"
        try:
            u=User.objects.create_user(username = request.data['correo'], password = request.data['password'], email = request.data['correo'], first_name=request.data['nombre'], last_name="", is_active=0)
            UsersMetadata.objects.create(token=token, user_id=u.id)
            
            html=f""" 
            <h3>Verificación de cuenta</h3>
               Hola {request.data['nombre']} te haz registrado exitosamente. Para activar tu cuenta haz clic en el siguiente enlace<br/>
               <a href="{url}">{url}</a>
               <br/>
               o copia y pega la siguiente URL en tu navegador favorito
               <br/>
               {url}
            """
            utilidades.sendMail(html, 'Prueba curso', request.data['correo'])
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"estado":"ok", "mensaje":"Se creó el registro exitosamente"}, status=HTTPStatus.CREATED)



class Clase2(APIView):
    
    
    def get(self, request, token):
        if token==None or not token:
            return JsonResponse({"estado":"error", "mensaje":"El campo password es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        try:
            data = UsersMetadata.objects.filter(token=token).get()
            UsersMetadata.objects.filter(token=token).update(token="")
            User.objects.filter(id=data.user_id).update(is_active=1)
            return HttpResponseRedirect(os.getenv('BASE_URL_FRONTEND'))
        except UsersMetadata.DoesNotExist:
            raise Http404
        

class Clase3(APIView):
    
    
    def post(self, request):
        if request.data.get("correo")==None or not request.data.get("correo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo correo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password")==None or not request.data.get("password"):
            return JsonResponse({"estado":"error", "mensaje":"El campo password es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        
        try:
            user = User.objects.filter(email=request.data.get('correo')).get()
        except User.DoesNotExist:
            raise Http404
        
        
        auth = authenticate(request, username=request.data.get("correo"), password=request.data.get("password"))
        if auth is not None:
            fecha = datetime.now()
            despues = fecha + timedelta(days=1)
            fecha_numero=int(datetime.timestamp(despues))
            payload = {"id":user.id,"IIS": os.getenv('BASE_URL'), "iat":int(time.time()), "exp":int(fecha_numero) }
            try:
                token= jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id":user.id, "nombre":user.first_name, "token":token},  status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":f"Ocurrió un error inesperado {e}"},  status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"estado":"error", "mensaje":"Las credenciales ingresadas no son válidas"},  status=HTTPStatus.BAD_REQUEST)
        