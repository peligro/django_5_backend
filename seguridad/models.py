from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersMetadata(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    token = models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.user.first_name}"

    class Meta:
        db_table = 'users_metadata'
        verbose_name = 'User metadata'
        verbose_name_plural = 'User metadata'