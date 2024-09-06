from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nome')
    position = models.CharField(max_length=100, verbose_name='Cargo')
    wage = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Remuneração')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    contact = models.TextField(verbose_name='Contato')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']