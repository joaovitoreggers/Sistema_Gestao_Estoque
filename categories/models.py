from django.db import models
from companies.models import Company

class Category(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='categories',
        verbose_name='Compania',
        null=True,
        blank=True
    )
        
    name = models.CharField(
        max_length=500, 
        verbose_name='Nome'
        )
    description = models.TextField(
        null=True, blank=True, 
        verbose_name='Descrição'
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
        verbose_name = 'Categoria'

    def __str__(self):
        return self.name
    