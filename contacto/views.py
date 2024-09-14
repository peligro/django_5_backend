from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from http import HTTPStatus
from datetime import datetime

#llamamos a utilidades
from utilidades import utilidades


#swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    
    @swagger_auto_schema(
        operation_descripcion="Endpoint para Contacto",
        responses={
            200:"Success",
            400:"Bad request"
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre':openapi.Schema(type=openapi.TYPE_STRING, description="Nombre"),
                'correo':openapi.Schema(type=openapi.TYPE_STRING, description="E-Mail"),
                'telefono':openapi.Schema(type=openapi.TYPE_STRING, description="Teléfono"),
                'mensaje':openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje")  
            },
            required=['nombre', 'correo', 'telefono', 'mensaje']
        )
    )
    def post(self, request):
        if request.data.get("nombre")==None or not request.data['nombre']:
            return JsonResponse({"estado":"error", "mensaje":"El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("correo")==None or not request.data['correo']:
            return JsonResponse({"estado":"error", "mensaje":"El campo correo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("telefono")==None or not request.data['telefono']:
            return JsonResponse({"estado":"error", "mensaje":"El campo telefono es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("mensaje")==None or not request.data['mensaje']:
            return JsonResponse({"estado":"error", "mensaje":"El campo mensaje es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        
        try:
            Contacto.objects.create(nombre=request.data['nombre'], correo=request.data['correo'], telefono=request.data['telefono'], mensaje=request.data['mensaje'], fecha=datetime.now())
            
            html=f""" 
                <h1>Nuevo mensaje de sitio web</h1>
                <ul>
                    <li>Nombre: {request.data['nombre']}</li>
                    <li>E-Mail: {request.data['correo']}</li>
                    <li>Teléfono: {request.data['telefono']}</li>
                    <li>Mensaje: {request.data['mensaje']}</li>
                </ul>
            """
            utilidades.sendMail(html, "Prueba curso", request.data['correo'])
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrió un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        

        
        return JsonResponse({"estado":"ok", "mensaje":"Se crea el registro exitosamente"}, status=HTTPStatus.OK)

