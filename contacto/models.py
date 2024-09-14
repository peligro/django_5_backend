from django.db import models

# Create your models here.
class Contacto(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    mensaje= models.TextField()
    fecha = models.DateTimeField()
    
    
    def __str__(self):
        return self.nombre
    
    
    class Meta:
        db_table = 'contacto'
        verbose_name="Contacto"
        verbose_name_plural = "Contactos"
    