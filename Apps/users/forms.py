from typing import Any
from django import forms
from .models import CustomUser
class UserForm(forms.ModelForm):
    """UserForm definition."""
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','image','username','password','groups']
        exclude=['user_permissions','last_login','date_joined','is_superuser','is_active','is_staff']
        # labels={
        #     'first_name':'first_name'
        # }
        widgets={
            'first_name':forms.TextInput(attrs={
                'placeholder':'Enter your name',
                'class':'form-control',
                'autofocus':True
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder':'Enter your last name',
                 'class':'form-control',
            }),
            'email':forms.EmailInput(attrs={
                 'class':'form-control',
                'placeholder':'Enter your email'

            }),
             'image':forms.FileInput(attrs={
                 'class':'form-control',
            }),
            'username':forms.TextInput(attrs={
                 'class':'form-control',
                'placeholder':'Enter your username'
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your password'
            }),

        }
    def clean_username(self) -> dict[str, Any]:
        username=self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists")
        return username 
    def clean_email(self):
        email=self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email  
    
class UserUpdateForm(forms.ModelForm):
    """UserForm definition."""
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','image','username','password']
        exclude=['groups','user_permissions','last_login','date_joined','is_superuser','is_active','is_staff']
        # labels={
        #     'first_name':'first_name'
        # }
        widgets={
            'first_name':forms.TextInput(attrs={
                'placeholder':'Enter your name',
                'class':'form-control',
                'autofocus':True
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder':'Enter your last name',
                 'class':'form-control',
            }),
            'email':forms.EmailInput(attrs={
                 'class':'form-control',
                'placeholder':'Enter your email'

            }),
             'image':forms.FileInput(attrs={
                 'class':'form-control',
            }),
            'username':forms.TextInput(attrs={
                 'class':'form-control',
                'placeholder':'Enter your username'
            }),
            'password':forms.PasswordInput(render_value=True,attrs={
                'class':'form-control',
                'placeholder':'Enter your password'
            }),

        }
       