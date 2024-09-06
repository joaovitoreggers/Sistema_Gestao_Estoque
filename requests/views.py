from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from . import models, forms

class RequestListView(ListView):
    model = models.Request
    template_name = 'request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        command_number = self.request.GET.get('command_number')

        if command_number:
            queryset = queryset.filter(name__icontains=command_number)
        return queryset
    
class RequestCreateView(CreateView):
    model = models.Request
    template_name = 'request_create.html'
    form_class = forms.RequestForm
    success_url = reverse_lazy('request_list')

class RequestDetailView(DetailView):
    model = models.Request
    template_name = 'request_detail.html'
    context_object_name = 'requests'

class RequestUpdateView(UpdateView):
    model = models.Request
    template_name = 'request_update.html'
    form_class = forms.RequestForm
    success_url = reverse_lazy('request_list')
    context_object_name = 'requests'

class RequestDeleteView(DeleteView):
    model = models.Request
    template_name = 'request_delete.html'
    success_url = reverse_lazy('request_list')
    context_object_name = 'requests'
