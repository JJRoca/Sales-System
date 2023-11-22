from django.contrib import admin
from .models import Category,Product
# Register your models here.
admin.site.register(Category)

class AdminProduct(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('id','name','category','price')
admin.site.register(Product,AdminProduct)
