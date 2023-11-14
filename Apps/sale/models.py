from django.db import models
from datetime import datetime

# Create your models here.
#categoria,producto,cliente,sale,dateSale
# class Employee(models.Model):
#     categ=models.ManyToManyField(Category)
#     names=models.CharField(max_length=150)
#     dni=models.CharField(max_length=10,unique=True)
#     date_joined=models.DateTimeField(default=datetime.now,verbose_name="Fecha de registro")
#     date_creation=models.DateTimeField(auto_now=True)
#     date_updated=models.DateTimeField(auto_now_add=True)
#     age=models.PositiveIntegerField(default=0)
#     salary=models.DecimalField(default=0.00,max_digits=9,decimal_places=2)
#     state=models.BooleanField(default=True)
#     '                                   "avatar/%Y/%m/%d"'
#     avatar=models.ImageField(upload_to='avatar',null=True,blank=True)
#     curriculum=models.FileField(upload_to='curriculum',null=True,blank=True)

#     def __str__(self):
#         return self.names
#     class Meta:
#         verbose_name="Empleado"
#         verbose_name_plural="Empleados"      
#         db_table='Empleado'

from Apps.categories.models import Product
from Apps.clients.models import Client
from django.forms import model_to_dict
class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.13, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.name
    
    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
