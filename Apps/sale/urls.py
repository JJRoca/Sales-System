from django.urls import path
from . import views
app_name='sale'
urlpatterns = [
    path('sale/get_id/',views.get_sale),
    path('sale/list/', views.SaleListView.as_view(), name='sale_list'),
    path('venta/',views.SaleCreateView.as_view(),name='hola'),
    path('search/',views.search_products, name='searchProducts'),

    path('get-product-details/',views.visualizar,name='visualizar'),

    #Generate PDF
    path('pdf/<int:id>/',views.generate_pdf,name='pdf'),

    path('sale/reports',views.GenerateReportListView.as_view(),name='reports'),

    #dashboard
    path('dashboard/',views.dashboard,name='dashboard')
]