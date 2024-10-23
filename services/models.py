from django.db import models
from companies.models import Company


class Service(models.Model):

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='service',
        verbose_name='Compania',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=500,
        verbose_name='Nome'
    )
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name='Valor do Serviço'
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
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f'{self.name} - {self.quantity}'  # Corrigido o erro no retorno