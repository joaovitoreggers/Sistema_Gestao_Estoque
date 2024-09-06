from django import forms
from . import models

class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = models.Employee
        fields = ['name', 'position', 'wage', 'description', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'wage': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }