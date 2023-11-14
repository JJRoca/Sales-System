from django.contrib import admin
from .models import Sale,DetSale
# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('pk','cli','subtotal','iva','total','date_joined')

admin.site.register(Sale, SaleAdmin)

class DetailAdmin(admin.ModelAdmin):
    list_display=["sale","prod","cant","price","subtotal"]
admin.site.register(DetSale,DetailAdmin)
