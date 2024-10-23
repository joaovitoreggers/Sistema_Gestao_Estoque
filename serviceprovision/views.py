from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from core import metrics
from . import models
from . import forms

from mixins import CompanyFilterMixin, PermissionsCreateMixin

class ServiceProvisionListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.ServiceProvision
    template_name = 'service_provision_list.html'
    context_object_name = 'service_provision'  
    paginate_by = 10
    permission_required = 'services.view_Service'

    def get_queryset(self):
        queryset = models.ServiceProvision.objects.all()
        service = self.request.GET.get('service')
        if service:
            queryset = queryset.filter(services__name__icontains=service).distinct()
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_provision'] = self.get_queryset() 
        context['sales_metrics'] = metrics.get_sales_metrics()
        return context


class ServiceProvisionCreateView(PermissionsCreateMixin, CreateView):
    model = models.ServiceProvision
    template_name = 'service_provision_create.html'
    form_class = forms.ServiceProvisionForm
    success_url = reverse_lazy('service_provision_list')
    permission_required = 'services.add_Service'
    context_object_name = 'service_provision'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscar todos os serviços disponíveis
        context['services'] = models.Service.objects.all()
        return context

    def form_valid(self, form):
        selected_services = self.request.POST.get('selected_services', '').split(',')
        quantities = self.request.POST.get('quantities', '').split(',')

        if selected_services and all(quantities) and len(selected_services) == len(quantities):
            total_value = 0

            # Buscar todos os serviços em uma única consulta
            services = models.Service.objects.filter(id__in=selected_services)
            services_to_add = []

            # Verifica os serviços selecionados e calcula o valor total
            for service, quantity in zip(services, quantities):
                if not quantity.isdigit():
                    messages.error(self.request, f'Quantidade inválida para o serviço {service.name}.')
                    return self.form_invalid(form)
                services_to_add.append(service)
                total_value += service.value * int(quantity)

            # Salva a prestação de serviços
            self.object = form.save(commit=False)
            self.object.value = total_value
            self.object.save()

            # Adiciona os serviços ao campo ManyToMany
            self.object.services.set(services_to_add)

            # Relaciona os serviços com a prestação através da tabela OutflowService
            for service, quantity in zip(services, quantities):
                models.OutflowService.objects.create(
                    service_provision=self.object,
                    service=service,
                    quantity=int(quantity)
                )

            messages.success(self.request, 'Prestação de serviços registrada com sucesso.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Erro ao processar os serviços selecionados.')
            return self.form_invalid(form)



class ServiceProvisionDetail(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.ServiceProvision
    template_name = 'service_provision_detail.html'
    context_object_name = 'service_provision'
    permission_required = 'services.view_service'

