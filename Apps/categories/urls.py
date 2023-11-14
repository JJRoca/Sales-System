from django.urls import path
from . import views

app_name="categories"
urlpatterns = [
    #PATH CATEGORIES
    path('category/list/',views.listaCategories,name="listaCategories"),
    # path('category/lista/',views.lista,name='list'),
    path('category/add/',views.CategoryCreateView.as_view(),name='category_create'),
    path('category/edit/<int:pk>/',views.CategoryUpdateView.as_view(),name='category_update'),
    path('category/delete/<int:pk>/',views.CategoryDeleteView.as_view(),name='category_delete'),
    
    #PATH PRODUCTS
    path('product/list/',views.ProductListView.as_view(),name='product_list'),
    path('product/create/',views.ProductCreateView.as_view(),name='product_create'),    
    path('product/edit/<int:pk>/',views.ProductUpdateView.as_view(),name='product_update'),
    path('product/delete/<int:pk>/',views.ProductDeleteView.as_view(),name='product_delete'),
    

]