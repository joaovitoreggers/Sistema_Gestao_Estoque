from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from . import models, forms

from mixins import CompanyFilterMixin, PermissionsCreateMixin

class SupplierListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin ,ListView):
    model = models.Suppliers
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    permission_required = 'suppliers.view_suppliers'


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class SupplierCreateView(PermissionsCreateMixin, CreateView):
    model = models.Suppliers
    form_class = forms.SupplierForm
    template_name = 'supplier_create.html'
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'
    permission_required = 'suppliers.add_suppliers'



class SupplierDetailView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Suppliers
    template_name = 'supplier_detail.html'
    context_object_name = 'suppliers'
    permission_required = 'suppliers.view_suppliers'


class SupplierUpdateView(PermissionsCreateMixin, UpdateView):
    model = models.Suppliers
    template_name = 'supplier_update.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'
    permission_required = 'suppliers.change_suppliers'



class SupplierDeleteVIew(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DeleteView):
    model = models.Suppliers
    template_name = 'supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'
    permission_required = 'suppliers.delete_suppliers'
