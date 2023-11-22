from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    image=models.ImageField(upload_to='',null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Verifica si es un usuario nuevo
            self.set_password(self.password)
        elif self.pk is not None:  # Verifica si es una actualización
            original = CustomUser.objects.get(pk=self.pk)
            if original.password != self.password:  # Verifica si la contraseña ha cambiado
                self.set_password(self.password)
        super().save(*args, **kwargs)  

    # def __str__(self):
    #     return self.get_full_name()    