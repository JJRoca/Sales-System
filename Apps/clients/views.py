from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,DeleteView
from .models import Client
from .forms import ClientForm
import logging
# Create your views here.

#list views for Clients
class ClientListView(ListView):
    model = Client
    template_name = "Clients/list.html"
    context_object_name='cli'
    http_method_names=["get","post"]
    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs) 
    #     context["prueba"]="new"
    #     context["form"]=self.request.POST
    #     print("contenido",context)
    #     return context
    
#create a new client

class ClientCreateView(CreateView):
    model = Client
    # fields=['names','surnames','dni','date_birthday','address','gender']
    form_class=ClientForm
    template_name = "Clients/create.html"
    success_url=reverse_lazy('client:client_list')
    def form_valid(self, form):
        if form.is_valid():
            print("formulario validado")
            form.save()
        else:
            print("error")
        return super().form_valid(form)


#delete a cliente
class ClientDeleteView(DeleteView):
    model = Client
    template_name = "Clients/delete.html"
    success_url=reverse_lazy('client:client_list')
    context_object_name="cli"
