# Generated by Django 5.1 on 2024-10-04 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Título')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('serie_number', models.CharField(max_length=200, verbose_name='Número de Série')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Preço de Compra')),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Preço de Venda')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='brands.brand', verbose_name='Marca')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='categories.category')),
            ],
            options={
                'verbose_name': 'Produto',
                'ordering': ['title'],
            },
        ),
    ]
