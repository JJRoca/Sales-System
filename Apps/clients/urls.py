from django.urls import path
from . import views
app_name='client'
urlpatterns = [
    path('clients/list/',views.ClientListView.as_view(),name='client_list'),
    path('clients/create/',views.ClientCreateView.as_view(),name='client_create'),
    path('clients/delete/<int:pk>',views.ClientDeleteView.as_view(),name='client_delete')

]