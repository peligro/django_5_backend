from django.urls import path , re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
 
#https://medium.com/django-unleashed/interactive-api-documentation-with-django-rest-framework-and-swagger-29222251ede8
#https://drf-yasg.readthedocs.io/en/stable/
schema_view = get_schema_view(
   openapi.Info(
      title="Curso Fullstack Django + DjangoRestFramewor + Vue",
      default_version='v1',
      description="API desarrollada para implementación de Backend de sistema de recetas, para curso Fullstack",
      terms_of_service="https://www.cesarcancino.com/cursos-en-udemy/",
      contact=openapi.Contact(email="yo@cesarcancino.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
	path('', home_inicio, name="home_inicio"),
 	path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
 
]