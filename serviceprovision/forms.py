from django import forms
from .models import ServiceProvision

class ServiceProvisionForm(forms.ModelForm):
    class Meta:
        model = ServiceProvision
        fields = ['client', 'employee', 'table', 'value', 'description']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'table': forms.NumberInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'id': 'value-input', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }