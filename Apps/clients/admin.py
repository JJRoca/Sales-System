from django.contrib import admin
from .models import Client
# Register your models here.
class AdminClient(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('id','name','surnames','dni')
 
admin.site.register(Client,AdminClient)