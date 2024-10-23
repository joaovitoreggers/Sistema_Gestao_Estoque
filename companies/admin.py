from django.contrib import admin
from . import models

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('company', 'user')
    search_fields = ('company', 'user')

admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.CompanyUser, CompanyUserAdmin)
