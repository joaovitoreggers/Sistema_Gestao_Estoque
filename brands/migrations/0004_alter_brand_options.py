# Generated by Django 5.1 on 2024-08-29 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0003_rename_suppliers_brand'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['name'], 'verbose_name': 'Marca'},
        ),
    ]