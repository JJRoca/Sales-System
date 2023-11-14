from django.db import models
from django.forms import model_to_dict
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150,unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    stock = models.IntegerField(default=0, verbose_name='Stock')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']
