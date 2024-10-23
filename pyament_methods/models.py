from django.db import models
from django.contrib.auth.models import User

from companies.models import Company

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('boleto', 'Boleto'),
        ('pix', 'Pix'),
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('cash', 'Dinheiro'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('succeeded', 'Sucesso'),
        ('failed', 'Falhou'),
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name='payments' ,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    transaction_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )  # Para armazenar o ID da transação da Stripe
    error_message = models.TextField(
        null=True, 
        blank=True
    )  # Para registrar mensagens de erro
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.amount} - {self.payment_method} - {self.status} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
