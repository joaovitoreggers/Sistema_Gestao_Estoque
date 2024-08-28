from django.contrib import admin
from .models import Inflow

class OutflowAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'description', 'created_at', 'updated_at',)

admin.site.register(Inflow, OutflowAdmin)

