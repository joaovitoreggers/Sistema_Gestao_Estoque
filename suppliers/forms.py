from django import forms
from . import models

class SupplierForm(forms.ModelForm):
    
    class Meta:
        model = models.Suppliers
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }