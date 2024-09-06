from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Clientes')
    phone_number = models.CharField(max_length=20, verbose_name='Número de telefone ')
    email = models.CharField(max_length=200, verbose_name='E-Mail')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    adress = models.CharField(max_length=400, verbose_name='Endereço')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['name']