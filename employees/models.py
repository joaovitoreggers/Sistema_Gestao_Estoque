from django.db import models
from companies.models import Company

class Employee(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='employees',
        verbose_name='Compania',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=250, 
        verbose_name='Nome'
        )
    position = models.CharField(
        max_length=100, 
        verbose_name='Cargo'
        )
    wage = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        verbose_name='Remuneração'
        )
    description = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Descrição'
        )
    contact = models.TextField(
        verbose_name='Contato'
        )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Criado em'
        )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Atualizado em'
        )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name