from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from companies.models import CompanyUser
from products.models import Product
from core import metrics
from . import models
from . import forms

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Outflow, Product

from mixins import CompanyFilterMixin, PermissionsCreateMixin


class OutflowListView(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10
    permission_required = 'outflows.view_outflow'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtra Outflows pela companhia do usuário logado
        company_user = get_object_or_404(CompanyUser, user=self.request.user)
        queryset = queryset.filter(company=company_user.company)  # Filtrando pelos Outflows da companhia do usuário

        product = self.request.GET.get('product')
        if product:
            queryset = queryset.filter(product__title__icontains=product)

        return queryset

    def get_context_data(self, **kwargs):

        company_user = getattr(self.request.user, 'profile', None)
        company = company_user.company if company_user else None

        context = super().get_context_data(**kwargs)
        context['products'] = list(Product.objects.values('id', 'title', 'selling_price'))
        context['sales_metrics'] = metrics.get_sales_metrics(company) if company else {}
        return context

    

class OutflowCreateView(PermissionsCreateMixin, CreateView):
    model = models.Outflow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflow_list')
    permission_required = 'outflows.add_outflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = list(Product.objects.values('id', 'title', 'selling_price'))
        return context

    def form_valid(self, form):
        selected_products = self.request.POST.get('selected_products', '').split(',')
        quantities = self.request.POST.get('quantities', '').split(',')

        if not selected_products or not all(quantities) or len(selected_products) != len(quantities):
            messages.error(self.request, 'Erro ao processar os produtos e as quantidades.')
            return redirect('outflow_create')

        try:
            total_value, total_quantity = self.calculate_total(selected_products, quantities)

            # Salva o objeto Outflow sem commit inicial
            self.object = form.save(commit=False)
            self.object.value = total_value
            self.object.quantity = total_quantity
            self.object.save()

            # Cria registros de OutflowProduct e atualiza a quantidade dos produtos
            self.create_outflow_products(selected_products, quantities)

            # Associa os produtos com o objeto de saída
            self.object.product.set(selected_products)

            return super().form_valid(form)

        except Product.DoesNotExist:
            messages.error(self.request, 'Um ou mais produtos não foram encontrados.')
            return redirect('outflow_create')

        except ValueError as e:
            messages.error(self.request, str(e))
            return redirect('outflow_create')

    def calculate_total(self, selected_products, quantities):
        """Calcula o valor total e a quantidade total dos produtos selecionados."""
        total_value = 0
        total_quantity = 0

        # Busca todos os produtos em uma única consulta
        products = Product.objects.filter(id__in=selected_products)

        for product_id, quantity in zip(selected_products, quantities):
            product = products.get(id=product_id)

            if product.quantity < int(quantity):
                raise ValueError(f'Quantidade insuficiente para o produto {product.title}. Estoque atual: {product.quantity}.')

            total_value += product.selling_price * int(quantity)
            total_quantity += int(quantity)

        return total_value, total_quantity

    def create_outflow_products(self, selected_products, quantities):
        """Cria os registros de OutflowProduct e atualiza a quantidade dos produtos."""
        products = Product.objects.filter(id__in=selected_products)

        for product_id, quantity in zip(selected_products, quantities):
            product = products.get(id=product_id)

            models.OutflowProduct.objects.create(
                outflow=self.object,
                product=product,
                quantity=int(quantity)
            )

            # Atualiza a quantidade do produto
            product.quantity -= int(quantity)
            product.save()


class OutflowDetail(LoginRequiredMixin, CompanyFilterMixin, PermissionRequiredMixin, DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflows'
    permission_required = 'outflows.view_outflow'