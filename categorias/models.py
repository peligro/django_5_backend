from django.db import models
from autoslug import AutoSlugField

# Create your models here.


class Categoria(models.Model):
    nombre=models.CharField(max_length=100, null=False)
    slug=AutoSlugField(populate_from='nombre')

    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'categorias'
        verbose_name='Categoría'
        verbose_name_plural='Categorías'