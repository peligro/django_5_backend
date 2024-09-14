from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#openapi swagger
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view=get_schema_view(
    openapi.Info(
        title="Curso Fullstack Django + DjangoRestFramework + Vue",
        default_version='v1',
        description="Api desarrollada para implementación de Backend de sistema de recetas, para curso Fullstack",
        terms_of_service="https://www.cesarcancino.com/cursos-en-udemy/",
        contact=openapi.Contact(email="yo@cesarcancino.com"),
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/v1/', include('ejemplo.urls')),
    path('api/v1/', include('categorias.urls')),
    path('api/v1/', include('recetas.urls')),
    path('api/v1/', include('contacto.urls')),
    path('api/v1/', include('seguridad.urls')),
    path('api/v1/', include('recetas_helper.urls')),
    path('documentacion<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentacion/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
