from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from . import models, forms

class ClientListView(ListView):
    model = models.Client
    template_name = 'client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class ClientCreateView(CreateView):
    model = models.Client
    template_name = 'client_create.html'
    form_class = forms.ClientForm
    success_url = reverse_lazy('client_list')


class ClientDetailView(DetailView):
    model = models.Client
    template_name = 'client_detail.html'
    context_object_name = 'clients'


class ClientUpdateView(UpdateView):
    model = models.Client
    template_name = 'client_update.html'
    form_class = forms.ClientForm
    success_url = reverse_lazy('client_list')
    context_object_name = 'clients'


class ClientDeleteView(DeleteView):
    model = models.Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')
    context_object_name = 'clients'