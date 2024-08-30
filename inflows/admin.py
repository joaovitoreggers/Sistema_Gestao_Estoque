from django.contrib import admin
from .models import Inflow

class OutflowAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product', 'quantity', 'description', 'created_at', 'updated_at',)
    search_fields = ('suplier__name', 'product__title')


admin.site.register(Inflow, OutflowAdmin)

