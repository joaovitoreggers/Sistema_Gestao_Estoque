from rest_framework import generics

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from outflows.models import Outflow
from products.models import Product
from . import models, forms, serializers

from mixins import CompanyFilterMixin, PermissionsCreateMixin



class EmployeeListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    permission_required = 'employees.view_employee'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    

class EmployeeCreateView(PermissionsCreateMixin, CreateView):
    model = models.Employee
    template_name = 'employee_create.html'
    form_class = forms.EmployeeForm
    success_url = reverse_lazy('employee_create')
    permission_required = 'employees.add_employee'


class EmployeeDetailView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employees'
    permission_required = 'employees.view_employee'


class EmployeeUpdateView(PermissionsCreateMixin, UpdateView):
    model = models.Employee
    template_name = 'employee_update.html'
    form_class = forms.EmployeeForm
    success_url = reverse_lazy('employee_list')
    context_object_name = 'employees'
    permission_required = 'employees.change_employee'


class EmployeeDeleteView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DeleteView):
    model = models.Employee
    template_name = 'employee_delete.html'
    success_url = reverse_lazy('employee_list')
    context_object_name = 'employees'
    permission_required = 'employees.delete_employee'

class EmployeeFilterView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Employee
    template_name = 'employee_filter.html'
    context_object_name = 'employees'
    permission_required = 'employees.view_employee'

    def get_queryset(self):
        # Filtra funcionários de acordo com o ID passado na URL
        queryset = models.Employee.objects.all()
        employee_id = self.request.GET.get('employees')

        if employee_id and employee_id.isdigit():
            queryset = queryset.filter(id=employee_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.request.GET.get('employees')
        selected_employee = None
        products = []
        outflows = []

        if employee_id and employee_id.isdigit():
            try:
                selected_employee = models.Employee.objects.get(id=employee_id)

                # Obtendo as vendas (Outflows) associadas ao funcionário
                outflows = Outflow.objects.filter(employee=selected_employee)

                # Coletando produtos das vendas (Outflows)
                for outflow in outflows:
                    products += [outflow_product.product for outflow_product in outflow.outflowproduct_set.all()]

                # Verifica se há produtos coletados
                if not products:
                    products = []  # Não exibe 'Nenhum produto encontrado'

            except models.Employee.DoesNotExist:
                selected_employee = None

        context['employees'] = models.Employee.objects.all()
        context['selected_employee'] = selected_employee
        context['filter_type'] = self.request.GET.get('filter')
        context['total_value'] = {outflow.id: outflow.total_value() for outflow in Outflow.objects.all()}

        # Filtra vendas e produtos conforme o funcionário selecionado
        context['products'] = products
        context['outflows'] = outflows

        return context

    
class CategoryCreateListApiView(generics.ListCreateAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

class CategoryRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer