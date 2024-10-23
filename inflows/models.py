from django.db import models
from companies.models import Company
from suppliers.models import Suppliers
from products.models import Product

class Inflow(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='inflows',
        verbose_name='Compania',
        null=True,
        blank=True
    )
    supplier = models.ForeignKey(
        Suppliers,
        on_delete=models.PROTECT, 
        related_name='inflow', 
        verbose_name='Fornecedor'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        verbose_name='Produto'
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
        verbose_name = 'Entrada'

    def __str__(self):
        return self.product.title