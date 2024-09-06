from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from . import models, forms

class EmployeeListView(ListView):
    model = models.Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class EmployeeCreateView(CreateView):
    model = models.Employee
    template_name = 'employee_create.html'
    form_class = forms.EmployeeForm
    success_url = reverse_lazy('employee_list')

class EmployeeDetailView(DetailView):
    model = models.Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employees'

class EmployeeUpdateView(UpdateView):
    model = models.Employee
    template_name = 'employee_update.html'
    form_class = forms.EmployeeForm
    success_url = reverse_lazy('employee_list')
    context_object_name = 'employees'

class EmployeeDeleteView(DeleteView):
    model = models.Employee
    template_name = 'employee_delete.html'
    success_url = reverse_lazy('employee_list')
    context_object_name = 'employees'
