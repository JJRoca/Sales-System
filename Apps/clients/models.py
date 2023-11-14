from django.db import models
from django.forms import model_to_dict
from datetime import datetime
# Create your models here.
gender_choices = (
    ('male','Male'),
    ('female','Female'),
)

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name')
    surnames = models.CharField(max_length=150, verbose_name='Last Name')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Date of birth')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Address')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Gender')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} '.format(self.name, self.surnames)
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']