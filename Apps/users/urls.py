from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    # path("login/",views.LoginFormView.as_view(),name="login")   
    path("login/",views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout')
]