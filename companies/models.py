from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name='Compania'
    )
    stripe_account_id = models.CharField(
        max_length=255, 
        verbose_name='ID da Conta Stripe', 
        null=True, 
        blank=True
    )  # Adicione este campo
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Compania'
        verbose_name_plural = 'Companias'
    
    def __str__(self):
        return self.name
    
class CompanyUser(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Funcionário da Empresa',
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='company_employees',
        verbose_name='Empresa'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Funcionário da empresa'
        verbose_name_plural = 'Funcionários da Empresa'
    
    def __str__(self):
        return self.user.username