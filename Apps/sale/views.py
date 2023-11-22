from decimal import Decimal
from typing import Any
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,get_object_or_404
from django.db import transaction
from Apps.categories.models import Product
from django.http import HttpRequest, HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.generic import CreateView,ListView,TemplateView
from .forms import SaleForm
from .models import Sale,DetSale
from Apps.categories.models import Product
from Apps.clients.models import Client
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

class SaleListView(LoginRequiredMixin,ListView):
    model = Sale
    context_object_name='sale'
    template_name = "Sale/list.html"
    login_url='users:login'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="Sales list"
        return context
#request get for details sale of client
def get_sale(request):
    if request.method=='GET':
        id_sale=request.GET.get('sale_id')
        id_sale=int(id_sale)
        s=Sale.objects.get(id=id_sale)
        det_sale=DetSale.objects.filter(sale=s)
        lista=[]
        for d in det_sale:
            dic={}
            dic["cliente"]=d.sale.cli.name
            dic['name']=d.prod.name
            dic['category']=d.prod.category.name
            dic['price']=d.price
            dic['cantidad']=d.cant
            dic['subTotal']=d.subtotal
            lista.append(dic)
        return JsonResponse(lista,safe=False)    

class SaleCreateView(LoginRequiredMixin,CreateView):
    model = Sale
    form_class=SaleForm
    template_name = "Sale/create.html"
    success_url=reverse_lazy("sale:sale_list")
    login_url='users:login'
    # Function to calculate subtotal, IVA, and total for saving in the Sale model
    def calculate_subtotal_iva_total(self,produc,products_cant,iva):
        sub_total_sale=sum([prod.price*int(prod_cant) for prod,prod_cant in zip(produc,products_cant)])
        iva_calculate_sale=(sub_total_sale*iva)
        total_sale=sub_total_sale+iva_calculate_sale       
        return round(sub_total_sale,2),iva_calculate_sale,round(total_sale,2)
    
    def form_valid(self, form):        
        cli=form.cleaned_data.get('cli')
        # Gets a list of strings of IDs that are sent from the front-end of the table with the id=values
        products_ids=self.request.POST.getlist('id')
        # Gets a list of string of IDs that sent from the front-end of the table with id=values, 
        products_cants=self.request.POST.getlist('cantidad')
        
        try:
            #user a single query to fetch products by their Ids
            prod=Product.objects.filter(id__in=products_ids)
        except Product.DoesNotExist:
            return HttpResponse("Error: Any dates does not exists")
        
        # Calculate subtotal, VAT, and total
        sub_total_sale,iva_calculate_sale,total_sale=self.calculate_subtotal_iva_total(prod,products_cants,Decimal(0.13))
        #Make sure that the sale and the sale details are saved together; if one of them fails, neither the sale nor the details will be saved        
        with transaction.atomic():  
            #Save the Sale 
            sale_v=Sale(
                cli=cli,
                subtotal=sub_total_sale,
                iva=iva_calculate_sale,
                total=total_sale
            )
            sale_v.save()
            #Save the details 
            details=[]
            for produ,product_cant in zip(prod,products_cants):
                detail_sale=DetSale(
                    sale=sale_v,
                    prod=produ,
                    price=produ.price,
                    cant=int(product_cant),
                    subtotal=produ.price*int(product_cant)
                )
                details.append(detail_sale)    
            # Save all the details in a single step
            DetSale.objects.bulk_create(details)
        return HttpResponseRedirect(self.success_url)


#function for filter products 
@login_required(login_url='users:login')
def search_products(request):
    try:    
        name_product=request.GET.get('filter')
                
        if name_product:
            product_list=Product.objects.filter(name__icontains=name_product)
            lista=list(product_list.values())
            return JsonResponse(lista,safe=False)
        else:
            print("error")
            return JsonResponse({"error":"access denied"},status=400)
    except ObjectDoesNotExist:
        #handle the object not found
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        # handle other general exceptions here
        print("an error ocurred:", str(e))
        return JsonResponse({"error": "Request error"}, status=500)
@login_required(login_url='users:login')   
def visualizar(request):
    name=request.GET.get("name")
    name_value=Product.objects.get(name=name)
    data={"id":name_value.id,"name":name_value.name,"category":name_value.category.name,"stock":name_value.stock,"price":name_value.price}
    return JsonResponse(data)


def generate_pdf(request,id):
        if request.method =="GET":
            sale=Sale.objects.get(pk=id)
            # Obtén el contenido HTML de tu plantilla
            template = get_template('Sale/invoice.html')
            context={
            'sale':sale
            }
            html = template.render(context)  # Asegúrate de definir context adecuadamente

            # Crear un objeto HttpResponse con el tipo de contenido PDF
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'filename="detailSale.pdf"'

            # Convertir HTML a PDF
            pisa.CreatePDF(html, dest=response)

            return response
        
#View to generate sales reports

class GenerateReportListView(LoginRequiredMixin,ListView):
    model = Sale
    template_name = 'Sale/report.html'
    context_object_name='sa'
    login_url='users:login'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)       
        context['title']="Sales Report"
        return context

#DASHBOARD
class Dasboard(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"
    login_url='users:login'
    #create a function to filter year,month
    def get_graph_sales_year_month(self):
        data = []
        try:
            year=datetime.now().year
            for m in range(1, 13):
                # print(year,m)
                total=Sale.objects.filter(date_joined__year=year,date_joined__month=m).aggregate(Sum("total"))
                total_value = total["total__sum"] if total["total__sum"] is not None else 0
                # print("----",total_value)
                data.append(float(total_value))
        except Exception as e: 
            print("error",e)
        return data       
    #function to show a graph of product by month  
    def get_graph_products_year_month(self):
        data=[]
        year=datetime.now().year
        month=datetime.now().month
        try:
            for p in Product.objects.all():
                print(p.id)
                total=DetSale.objects.filter(sale__date_joined__year=year,sale__date_joined__month=month,prod__id=p.id).aggregate(Sum('subtotal'))
                print(total)
                total_values=total['subtotal__sum'] if total['subtotal__sum'] is not None else 0
                print("total-------",total_values)
                if total_values>0:
                    data.append({
                        'name':p.name,
                        'y':float(total_values)
                    })
        except Exception as e:
            pass    
        return data
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["year"]=self.get_graph_sales_year_month()
        product_year_month=self.get_graph_products_year_month()
        context["chart_data"]=product_year_month
        return context 