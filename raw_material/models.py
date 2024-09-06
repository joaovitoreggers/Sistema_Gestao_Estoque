from django.db import models
from categories.models import Category
from  brands.models import Brand

class RawMaterial(models.Model):
    name = models.CharField(max_length=500, verbose_name='Nome')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoria')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Marca')
    is_perecible = models.BooleanField(verbose_name='É prececível?')
    quantity = models.FloatField(verbose_name='Quantidade')
    cost_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Preço de Custo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']