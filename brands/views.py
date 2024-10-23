from rest_framework import generics

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from brands.serializers import BrandSerializer
from django.urls import reverse_lazy

from outflows.models import Outflow, OutflowProduct
from products.models import Product
from . import models, forms
from mixins import CompanyFilterMixin


class BrandListView(LoginRequiredMixin, CompanyFilterMixin, ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands' 
    paginate_by = 5
    permission_required = 'brands.view_brand'
    
    company_model = models.Brand

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    
class BrandCreateView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.add_brand'

    def form_valid(self, form):
        company_user = self.request.user.profile  
        form.instance.company = company_user.company
        
        return super().form_valid(form)

class BrandDetailView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brands'
    permission_required = 'brands.change_brand'


class BrandUpdateView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    context_object_name = 'brands'
    permission_required = 'brands.change_brand'


class BrandDeleteView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    success_url = reverse_lazy('brand_list')
    context_object_name = 'brands'
    permission_required = 'brands.create_brand'


class BrandFilterView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brand_filter.html'
    context_object_name = 'brands'
    paginate_by = 10
    permission_required = 'brands.view_brands'

    def get_queryset(self):
        queryset = models.Brand.objects.all()
        brand_id = self.request.GET.get('brands')

        if brand_id:
            queryset = queryset.filter(id=brand_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_id = self.request.GET.get('brands')
        selected_band = None
        products = []


        if brand_id:
            try:
                selected_band = models.Brand.objects.get(id=brand_id)
                products = selected_band.product.all() 

            except models.Brand.DoesNotExist:
                selected_band = None

        # Obtendo todas as marcas
        context['brands'] = models.Brand.objects.all()
        context['selected_band'] = selected_band
        context['filter_type'] = self.request.GET.get('filter')
        context['total_value'] = {outflow.id: outflow.total_value() for outflow in Outflow.objects.all()}

        # Filtrando os produtos da marca selecionada
        if selected_band:
            context['products'] = products 
            context['outflows'] = Outflow.objects.filter(
                outflowproduct__product__brand=selected_band
            ).distinct()
        else:
            context['products'] = Product.objects.none()  # Se nenhuma marca for selecionada
            context['outflows'] = Outflow.objects.none()  # Se nenhuma marca for selecionada

        return context

class BrandCreateListApiView(generics.ListCreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = BrandSerializer

class BrandRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = BrandSerializer