from rest_framework import generics

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render
from serviceprovision.models import ServiceProvision 
from outflows.models import Outflow 
from . import models, forms
from .import serializers

from mixins import PermissionsCreateMixin, CompanyFilterMixin





class ClientListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Client
    template_name = 'client_list.html'
    context_object_name = 'clients'
    paginate_by = 10
    permission_required = 'clients.view_client'


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class ClientCreateView(PermissionsCreateMixin, CreateView):
    model = models.Client
    template_name = 'client_create.html'
    form_class = forms.ClientForm
    success_url = reverse_lazy('client_list')
    permission_required = 'clients.add_client'


class ClientDetailView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Client
    template_name = 'client_detail.html'
    context_object_name = 'clients'
    permission_required = 'clients.view_client'



class ClientUpdateView(PermissionsCreateMixin, UpdateView):
    model = models.Client
    template_name = 'client_update.html'
    form_class = forms.ClientForm
    success_url = reverse_lazy('client_list')
    context_object_name = 'clients'
    permission_required = 'clients.change_client'



class ClientDeleteView(LoginRequiredMixin, CompanyFilterMixin, DeleteView):
    model = models.Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')
    context_object_name = 'clients'
    permission_required = 'clients.delete_client'

class ClientFilterView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, View):
    permission_required = 'clients.view_client'  # Permissão adequada

    def get(self, request):
        clients = models.Client.objects.all()
        selected_client = None
        outflows = []  # Lista para armazenar as compras
        service_provisions = []  # Lista para armazenar os serviços contratados

        client_id = request.GET.get('client')
        filter_type = request.GET.get('filter')  # Adiciona a captura do filtro

        if client_id:
            selected_client = models.Client.objects.get(id=client_id)

            # Obter todas as compras do cliente selecionado
            if filter_type == "purchase":
                outflows = Outflow.objects.filter(client=selected_client)
            elif filter_type == "service":
                service_provisions = ServiceProvision.objects.filter(client=selected_client)

        context = {
            'clients': clients,
            'selected_client': selected_client,
            'outflows': outflows,
            'service_provisions': service_provisions,  # Adiciona a lista de serviços ao contexto
            'filter_type': filter_type,  # Adiciona o tipo de filtro ao contexto
        }
        return render(request, 'client_filter.html', context)
    

class ClientCreateListApiView(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class ClientRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer