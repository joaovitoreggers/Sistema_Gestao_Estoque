from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from . import models, forms

from mixins import CompanyFilterMixin, PermissionsCreateMixin

class ServiceListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Service
    template_name = 'service_list.html'
    context_object_name = 'services' 
    paginate_by = 10
    permission_required = 'services.view_Service'


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    
class ServiceCreateView(PermissionsCreateMixin, CreateView):
    model = models.Service
    template_name = 'service_create.html'
    form_class = forms.ServiceForm
    success_url = reverse_lazy('service_list')
    permission_required = 'services.add_service'


class ServiceDetailView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Service
    template_name = 'service_detail.html'
    context_object_name = 'services'
    permission_required = 'services.change_service'


class ServiceUpdateView(PermissionsCreateMixin, UpdateView):
    model = models.Service
    template_name = 'service_update.html'
    form_class = forms.ServiceForm
    success_url = reverse_lazy('service_list')
    context_object_name = 'services'
    permission_required = 'services.change_service'

class ServiceDeleteView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DeleteView):
    model = models.Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')
    context_object_name = 'services'
    permission_required = 'services.create_service'
