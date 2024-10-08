from django import forms
from . import models

class ClientForm(forms.ModelForm):
    
    class Meta:
        
        model = models.Client
        fields = ['name', 'phone_number', 'email', 'description', 'adress']
       
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }