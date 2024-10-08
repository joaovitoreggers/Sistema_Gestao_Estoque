from django.db import models
from products.models import Product
from pyament_methods.models import Payament_method
from clients.models import Client
from employees.models import Employee

class Outflow(models.Model):
    product = models.ManyToManyField(
        Product,
        verbose_name='Produto'
        )
    payament_method = models.ForeignKey(
        Payament_method, 
        on_delete=models.PROTECT, 
        related_name='command', 
        verbose_name='Método de Pagamento',
        blank=True,
        null=True,
        )
    client = models.ForeignKey(
        Client, 
        on_delete=models.PROTECT, 
        related_name='command', 
        verbose_name='Cliente',
        blank=True,
        null=True,
        )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        related_name='command',
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
        verbose_name = 'Vendas'

    def __str__(self):
        return f'{self.id} - {self.client} - {self.created_at}' 
    

class OutflowProduct(models.Model):
    outflow = models.ForeignKey(Outflow, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantidade do produto na saída

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'
