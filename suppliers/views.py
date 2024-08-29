from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms

class SupplierListView(ListView):
    model = models.Suppliers
    template_name = 'supplier_list.html'
    context_object_name = 'brands'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
