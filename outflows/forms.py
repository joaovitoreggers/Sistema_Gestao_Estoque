from django.core.exceptions import ValidationError
from django import forms
from .models import Outflow

class OutflowForm(forms.ModelForm):
    class Meta:
        model = Outflow
        fields = ['description', 'client', 'employee', 'value']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'id': 'value-input', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
