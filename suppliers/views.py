from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms

class SupplierListView(ListView):
    model = models.Suppliers
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class SupplierCreateView(CreateView):
    model = models.Suppliers
    form_class = forms.SupplierForm
    template_name = 'supplier_create.html'
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'


class SupplierDetailView(DetailView):
    model = models.Suppliers
    template_name = 'supplier_detail.html'
    context_object_name = 'suppliers'


class SupplierUpdateView(UpdateView):
    model = models.Suppliers
    template_name = 'supplier_update.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'


class SupplierDeleteVIew(DeleteView):
    model = models.Suppliers
    template_name = 'supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
    context_object_name = 'suppliers'