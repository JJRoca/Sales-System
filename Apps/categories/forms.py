from django import forms
from django.utils.html import mark_safe
from django.conf import settings
from .models import Category,Product
class CategoryForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    class Meta:
        """Meta definition for MODELNAMEform."""
        model = Category
        fields = ['name','desc']
        labels={
            'name':"Name",
            'desc':'Description'
        }   
        widgets={
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'id':'name','placeholder':'Ingrese un nombre',
                'autocomplete':'off',
                'autofocus':True,
                }),
            'desc':forms.Textarea(attrs={
                'class':'form-control',
                'id':'desc','placeholder':'Ingrese una descripcion',
                'autocomplete':'off',
                'rows':3,
                'cols':3
            })    
        }

class ProductForm(forms.ModelForm):
    #error_messages="Error" 
    price = forms.DecimalField(
        max_digits=10,  # Número máximo de dígitos permitidos
        decimal_places=2,  # Número de lugares decimales
        widget=forms.TextInput(attrs={
            'id': 'price',
            'class': 'form-control',
            'placeholder': '0.00',
        })
    )
    class Meta:
        model = Product
        fields = ('name','category','image','price')
        labels={'name':'Name',
                'category':'Category',
                'image':'Image',
                'price':'Price'}
        widgets={
            'name':forms.TextInput(attrs={
                'id':'name',
                'class':'form-control',
                'placeholder':'Enter a product',
                # 'autofocus':True
            }),
            'category':forms.Select(attrs={
                'id':'category',
                'class':'form-control',
            }),
            'image':forms.FileInput(attrs={
                'id':'image',
                'class':'form-control',
            }),        
        }
    def clean_name(self):
        #check if fields are empty or no
        name=self.cleaned_data['name']
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError("this name already exists")
        return name
    def clean_price(self):
        price=self.cleaned_data['price']
        #check if price is more than 0
        if price<=0:
            
            raise forms.ValidationError("The price must be a positive value")
        return price
    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     print("imagen resuelta",image)
    #     if not image:
    #         print("entro")
    #         # Si no se proporciona una imagen, utiliza la imagen por defecto
    #         return settings.STATIC_URL + 'img/empty.png'
    #     return image.url

