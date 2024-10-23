from django.db import models
from companies.models import Company
from pyament_methods.models import Payment
from clients.models import Client
from employees.models import Employee
from services.models import Service

class ServiceProvision(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='service_provision',
        verbose_name='Compania',
        null=True,
        blank=True
    )
    services = models.ManyToManyField(  # Corrigido para plural
        Service,
        verbose_name='Serviços'
    )
    payament_method = models.ForeignKey(
        Payment, 
        on_delete=models.PROTECT, 
        related_name='provisions',  # Nome único
        verbose_name='Método de Pagamento',
        blank=True,
        null=True,
    )
    client = models.ForeignKey(
        Client, 
        on_delete=models.PROTECT, 
        related_name='provisions',  # Nome único
        verbose_name='Cliente',
        blank=True,
        null=True,
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        related_name='provisions',  # Nome único
        verbose_name='Funcionário',
        null=True,
        blank=True
    )
    table = models.CharField(
        max_length=200, 
        verbose_name='Mesa', 
        null=True, 
        blank=True
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total',
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(
        default=0, 
        verbose_name='Quantidade'
    )
    description = models.TextField(
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
        ordering = ['-created_at']
        verbose_name = 'Prestação de Serviços'

    def __str__(self):
        return f'{self.id} - {self.client} - {self.created_at}' 


class OutflowService(models.Model):
    service_provision = models.ForeignKey(  # Nome único e sem maiúscula
        ServiceProvision,  # Relacionamento correto com ServiceProvision
        on_delete=models.CASCADE,
        related_name='outflow_services'
    )
    service = models.ForeignKey(  # Corrigido para não sobrescrever
        Service, 
        on_delete=models.CASCADE,
        related_name='outflows'
    )
    quantity = models.PositiveIntegerField(
        default=1
    ) 
    
    class Meta:
        verbose_name = 'Serviço Já Prestado'
        verbose_name_plural = 'Serviços Já Prestados'

    def __str__(self):
        return f'{self.service.name} - {self.quantity}'
