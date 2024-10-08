from django.db import models

class Payament_method(models.Model):
    name = models.CharField(
        max_length=250, 
        verbose_name='Nome'
        )
    description = models.TextField(
        null=True,
        blank=True, 
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

        ordering = ['name']
    
    def __str__(self):
        return self.name