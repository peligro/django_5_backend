from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.http.response import JsonResponse
from http import HTTPStatus
from jose import jwt
from django.conf import settings
import time


def logueado(redirect_url=None):
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            #print(f"Authorization={req.headers.get('Authorization')}")
            if not req.headers.get('Authorization') or req.headers.get('Authorization')==None:
                return JsonResponse({"estado":"error", "mensaje":"Sin autorización"},  status=HTTPStatus.UNAUTHORIZED)
            header = req.headers.get('Authorization').split(" ")
            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])  
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":f"Sin autorización {e}"},  status=HTTPStatus.UNAUTHORIZED)
            if int(resuelto['exp'])>int(time.time()):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({"estado":"error", "mensaje":f"Sin autorización 3"},  status=HTTPStatus.UNAUTHORIZED)
            
        return _decorator
    return metodo


"""
def logueado(redirect_url=None):
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            print(f"Authorization={req.headers.get('Authorization')}")
            return func(request, *args, **kwargs)
        return _decorator
    return metodo
"""