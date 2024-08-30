from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from . import models
from . import forms

class InflowListView(ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('Product')

        if product:
            queryset = queryset.filter(Product__title__icontains=product)
        return queryset
    
class InflowCreateView(CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')

class InflowDetail(DetailView):
    model = models.Inflow
    template_name = 'inflow_detail'
    context_object_name = 'inflows'

