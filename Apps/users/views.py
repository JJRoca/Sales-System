from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.views import LoginView
# Create your views here.
# class LoginFormView(LoginView):
#     template_name="users/login.html"    
#     success_url=reverse_lazy("categories:listaCategories")
#     def post(self, request, *args, **kwargs):
#         username=self.request.POST['username']
#         s=self.request.POST.get('username')
#         if s is None:
#             print("error")
#         print(s+""+username)
#         print(request.POST)
#         return super().post(request, *args, **kwargs)
     
def loginUser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("logged in you in successfully", user.username,user.password)
            login(request,user)
            return redirect('categories:listaCategories')
        else:
            print("there was a authentication error")    
    
    return render(request, 'Users/login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")


               