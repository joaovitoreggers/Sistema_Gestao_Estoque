from django.db import models
from products.models import Product
from pyament_methods.models import Payament_method
from clients.models import Client
from employees.models import Employee

class Request(models.Model):
    product = models.ManyToManyField(Product, verbose_name='Produtos', related_name='command')
    total_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor Total')
    status = models.CharField(max_length=200, verbose_name='Status')
    payament_method = models.ForeignKey(Payament_method, on_delete=models.PROTECT, related_name='command', verbose_name='Método de Pagamento')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='command', verbose_name='Cliente')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='command')
    table = models.CharField(max_length=200, verbose_name='Mesa', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    is_delivery = models.BooleanField(verbose_name='É Entrega')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-id']