from django import forms
from . import models

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = models.Request
        fields = ['product', 'total_value', 'status', 'payament_method',
                  'client', 'employee', 'table', 'is_delivery', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'total_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'payament_method': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'table': forms.TextInput(attrs={'class': 'form-control'}),
            'is_delivery': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }