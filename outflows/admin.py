from django.contrib import admin
from .models import Outflow
from .models import SalesCounter

class OutflowAdmin(admin.ModelAdmin):
    list_display = ( 'quantity', 'description', 'created_at', 'updated_at')

admin.site.register(Outflow, OutflowAdmin)

# admin.py
from django.contrib import admin
from .models import SalesCounter

@admin.register(SalesCounter)
class SalesCounterAdmin(admin.ModelAdmin):
    list_display = ('total_sales', 'calculate_fee')
    readonly_fields = ('total_sales', 'calculate_fee')

    def has_add_permission(self, request):
        return False  # Evita criação de novos registros via Django Admin

    def has_delete_permission(self, request, obj=None):
        return False  # Evita a exclusão do contador via Django Admin
