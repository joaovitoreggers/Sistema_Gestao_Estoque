from django.shortcuts import get_object_or_404
from rest_framework import generics

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from companies.models import CompanyUser
from outflows.models import OutflowProduct, Outflow
from products.models import Product
from . import models, forms, serializers
from mixins import CompanyFilterMixin, PermissionsCreateMixin


class CategoryListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    permission_required = 'categories.view_category'


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class CategoryCreateView(PermissionsCreateMixin, CreateView):
    model = models.Category
    template_name = 'category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.add_category'

    def form_valid(self, form):
        user_company = getattr(self.request.user.profile, 'company', None)
        form.instance.company = user_company

        return super().form_valid(form)


class CategoryDetail(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Category
    template_name = 'category_detail.html'
    context_object_name = 'categories'
    permission_required = 'categories.view_category'


class CategorydUpdateView(PermissionsCreateMixin, UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')
    context_object_name = 'categories'
    permission_required = 'categories.change_category'



class CategoryDeleteView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')
    context_object_name = 'categories'
    permission_required = 'categories.delete_category'


class CategoryFilterView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'category_filter.html'
    context_object_name = 'products'
    permission_required = 'categories.view_category'

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        selected_category = None
        company_user = get_object_or_404(CompanyUser, user=self.request.user)
        categories = models.Category.objects.filter(company=company_user.company)  # Filtra categorias pela companhia do usuário

        if category_id:
            selected_category = get_object_or_404(models.Category, id=category_id)

        context['categories'] = categories
        context['selected_category'] = selected_category
        context['filter_type'] = self.request.GET.get('filter')
        context['total_value'] = {outflow.id: outflow.total_value() for outflow in Outflow.objects.all()}

        # Filtrando Outflows com base nos produtos da categoria selecionada
        context['outflows'] = Outflow.objects.filter(
            outflowproduct__product__category_id=selected_category.id
        ).distinct() if selected_category else Outflow.objects.none()

        return context

    
class CategoryCreateListApiView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CategoryRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer