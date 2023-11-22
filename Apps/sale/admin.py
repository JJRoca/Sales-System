from django.contrib import admin
from .models import Sale,DetSale
# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('pk','cli','subtotal','iva','total','date_joined')


admin.site.register(Sale, SaleAdmin)

class DetailAdmin(admin.ModelAdmin):
    list_display=["sale","prod","cant","price","subtotal","sale_date_joined"]
    def sale_date_joined(self, obj):
        return obj.sale.date_joined if obj.sale else None

    sale_date_joined.short_description = 'Fecha de venta'
admin.site.register(DetSale,DetailAdmin)
