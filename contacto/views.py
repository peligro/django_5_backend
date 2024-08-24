from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404
from http import HTTPStatus
from .models import *
import os
from dotenv import load_dotenv
from datetime import datetime
from utilidades import utilidades
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    
    
    @swagger_auto_schema(
        operation_description="Endpoint Operation Description",
        responses={
            200: "Success",
            400: "Bad Request",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Nombre"),
                'correo': openapi.Schema(
                    type=openapi.TYPE_STRING, description="E-Mail"),
                'telefono': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Teléfono"),
                'mensaje': openapi.Schema(
                    type=openapi.TYPE_STRING, description="Mensaje"),
            },
            required=['nombre', 'correo']
        )
    )
    def post(self, request):
        if request.data.get("nombre")==None or not request.data.get("nombre"):
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("correo")==None or not request.data.get("correo"):
            return JsonResponse({"estado":"error", "mensaje":"El campo correo es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("telefono")==None or not request.data.get("telefono"):
            return JsonResponse({"estado":"error", "mensaje":"El campo telefono es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        if request.data.get("mensaje")==None or not request.data.get("mensaje"):
            return JsonResponse({"estado":"error", "mensaje":"El campo mensaje es obligatorio"},  status=HTTPStatus.BAD_REQUEST)
        
        try:
            Contacto.objects.create(nombre=request.data['nombre'], correo = request.data['correo'], telefono = request.data['telefono'], mensaje = request.data['mensaje'], fecha=datetime.now())
            #nótese que si se envía sin la fecha, la toma del servidor
            #Contacto.objects.create(nombre=request.data['nombre'], correo = request.data['correo'], telefono = request.data['telefono'], mensaje = request.data['mensaje'])
            
            html=f""" 
            <h3>Nuevo registrado a evento</h3>
                <ul>
                    <li>Nombre: {request.data['nombre']}</li>
                    <li>E-Mail: {request.data['correo']}</li>
                    <li>Teléfono: {request.data['telefono']}</li>
                    <li>Mensaje: {request.data['mensaje']}</li>
                    </ul>
            """
            utilidades.sendMail(html, 'Prueba curso', request.data['correo'])
            
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"},  status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"estado":"ok", "mensaje":"Se creó el registro exitosamente"}, status=HTTPStatus.OK)

    