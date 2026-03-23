from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'image', 'description', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }