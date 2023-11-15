from django.shortcuts import render,get_list_or_404
from django.urls import reverse_lazy    
from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from .models import Category,Product
from .forms import CategoryForm,ProductForm
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

#Decorators are used to check if users are authenticated
@login_required(login_url='users:login')
def listaCategories(request):
    cat=Category.objects.all()
    list={"title":"List of categories",
          "cat":cat}
    return render(request,'Categories/list.html',list)

# vistas basadas en clases
# class CategoryListView(ListView):
#     model=Category
#     template_name="Categories/list.html"

#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context["title"]="List of categories"
#         return context

def lista(request):
    filter_id = request.GET.get('filter_id')
    if filter_id:
        try:
            cat = Category.objects.get(id=int(filter_id))
            print("*-----",type(cat))
            data = {'id': cat.id, 'name': cat.name}
            return JsonResponse(data)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    else:
        cat = Category.objects.all()
        list_data = {"title": "List of categories", "cat": cat}
        return render(request, 'Categories/list.html', list_data)
#Decorators are used to check if users are authenticated
@method_decorator(login_required(login_url='users:login'),name='dispatch')
class CategoryCreateView(CreateView):
    #define the model, template, form class for category creation
    model = Category    
    template_name = "Categories/create.html"
    form_class=CategoryForm  
    success_url=reverse_lazy('categories:listaCategories')
    def post(self, request, *args, **kwargs):
        # Create a new dictionary to send to the `jsonResponse()` function.
        data={}
        name=request.POST.get('name')
        #check if name is true
        if name:
            #check if category name already exists()
            category_exists=Category.objects.filter(name__exact=name).exists()
            print("entro",category_exists)
            if category_exists:
                data={"Error":"Category exixsts already"}
            else:
                form=self.form_class(request.POST)
                if form.is_valid():
                    # save the new category and prepare data for JSON response
                    category=form.save()
                    data={"id":category.id,"name":category.name,"desc":category.desc}             
        print(data)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        #define context data  for category creation view
        context=super().get_context_data(**kwargs)
        context["title"]="Creaction of a new category"
        return context


#Update view for categories with class-based view
#Decorators are used to check if users are authenticated
class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    template_name = "Categories/update.html"
    form_class=CategoryForm
    success_url=reverse_lazy('categories:listaCategories')
    login_url='users:login'

    # This method is used for fields validation
    def form_valid(self, form):
        form.save()
        message = 'Category updated successfully'
        # if the form is valid, return a JSON response indicating a successful category update      
        return JsonResponse({'success': True, 'message': message})
    def form_invalid(self, form):
        #if the form is invalid, return a JSON response instead of an error message in the form
        return JsonResponse({'success': False, 'errors': form.errors})
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        a=self.object
        context['title']='Update Category'
        context['a']=a
        return context

#Delete view for categories class-based view
#Decorators are used to check if users are authenticated
class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = "Categories/delete.html"
    context_object_name='f'
    success_url=reverse_lazy('categories:listaCategories')
    login_url='users:login'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Delete register'
        return context


#class-based-views of products

class ProductListView(ListView):
    model = Product
    template_name = "Products/list.html"
    context_object_name='producto'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']="List of Products"
        return context
    
# class-based-vews to create a product   
class ProductCreateView(CreateView):
    model=Product
    template_name='Products/create.html'
    form_class=ProductForm    
    success_url=reverse_lazy("categories:product_list")
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Creation of a new product'
        return context
    

#class-based-views to update a product
class ProductUpdateView(UpdateView):
    model = Product
    template_name = "Products/update.html"
    form_class=ProductForm
    success_url=reverse_lazy('categories:product_list')
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["title"]="Updated product"
        return context
#class-based-views to delete a product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "Products/delete.html"
    context_object_name='p'
    success_url=reverse_lazy('categories:product_list')
