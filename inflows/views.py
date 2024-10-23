from rest_framework import generics

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from . import models, forms, serializers

from mixins import CompanyFilterMixin, PermissionsCreateMixin


class InflowListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflows.view_inflow'


    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('Product')

        if product:
            queryset = queryset.filter(Product__title__icontains=product)
        return queryset
    
class InflowCreateView(PermissionsCreateMixin, CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflows.add_inflow'


class InflowDetail(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail'
    context_object_name = 'inflows'
    permission_required = 'inflows.delete_inflow'


   
class CategoryCreateListApiView(generics.ListCreateAPIView):
    queryset = models.Inflow.objects.all()
    serializer_class = serializers.InflowSerializer

class CategoryRetriveApiView(generics.RetrieveAPIView):
    queryset = models.Inflow.objects.all()
    serializer_class = serializers.InflowSerializer