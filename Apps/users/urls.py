from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path("login/",views.loginUser,name='login'),

    path('logout/',views.logoutUser,name='logout'),
    #path to create user
    path('user/create/',views.UserCreateView.as_view(),name='user_create'),
    #path to list user
    path('user/list/',views.UserListView.as_view(),name='user_list'),
    #path to update user
    path('user/update/<int:pk>',views.UserUpdateView.as_view(),name='user_update'),
    #path to delete user
    path('user/delete/<int:pk>',views.UserDeleteView.as_view(),name='user_delete')
]
