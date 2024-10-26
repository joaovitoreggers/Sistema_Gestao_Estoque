from django.db import models
from brands.models import Brand
from categories.models import Category
from companies.models import Company

class Product(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Compania',
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=500, 
        verbose_name='Título'
        )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.PROTECT, 
        related_name='product', 
        verbose_name='Marca'
        )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='product'
        )
    description = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Descrição'
        )
    serie_number = models.CharField(
        max_length=200, 
        verbose_name='Número de Série'
        )
    quantity = models.IntegerField(
        default=0, 
        verbose_name='Quantidade'
        )
    cost_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        verbose_name='Preço de Compra'
        )
    selling_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        verbose_name='Preço de Venda'
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
        
        ordering = ['title']
        verbose_name = 'Produto'

    def __str__(self):
        return self.title