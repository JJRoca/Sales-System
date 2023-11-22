from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import CustomUser
from django.contrib.auth.views import LoginView
from .forms import UserForm,UserUpdateForm
     
def loginUser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("logged in you in successfully", user.username,user.password)
            login(request,user)
            return redirect('sale:dashboard')
        else:
            print("there was a authentication error")    
    
    return render(request, 'Users/login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

#create View Users
#list users
class UserListView(ListView):
    model = CustomUser
    template_name = "Users/list.html"
    context_object_name="user"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='List of user'
        # print(context)
        return context

#creation of user
class UserCreateView(CreateView):
    model = CustomUser
    template_name = "Users/create.html"
    form_class=UserForm
    success_url=reverse_lazy('users:user_list')
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Creation of user'
        return context


#class-based-view to update user
class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = "Users/update.html"
    form_class=UserUpdateForm
    success_url=reverse_lazy('users:user_list')
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Update user'
        return context

#class-based-view to delete user
class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = "users:user_delete"

