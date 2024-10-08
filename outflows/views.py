from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from inflows.signals import update_product_quantity
from . import models
from . import forms
from products.models import Product
from core import metrics

class OutflowListView(ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.GET.get('product')
        if product:
            queryset = queryset.filter(product__title__icontains=product)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = list(Product.objects.values('id', 'title', 'selling_price'))
        context['sales_metrics'] = metrics.get_sales_metrics()
        return context

class OutflowCreateView(CreateView):
    model = models.Outflow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = list(Product.objects.values('id', 'title', 'selling_price'))
        return context

    class OutflowCreateView(CreateView):
        model = models.Outflow
        template_name = 'outflow_create.html'
        form_class = forms.OutflowForm
        success_url = reverse_lazy('outflow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = list(Product.objects.values('id', 'title', 'selling_price'))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        selected_products = self.request.POST.get('selected_products', '').split(',')
        quantities = self.request.POST.get('quantities', '').split(',')

        if selected_products and all(quantities) and len(selected_products) == len(quantities):
            total_value = 0
            total_quantity = 0

            for product_id, quantity in zip(selected_products, quantities):
                if product_id:
                    product = Product.objects.get(id=product_id)
                    total_value += product.selling_price * int(quantity)
                    total_quantity += int(quantity)

                    models.OutflowProduct.objects.create(
                        outflow=self.object,
                        product=product,
                        quantity=int(quantity)
                    )

                self.object.value = total_value
                self.object.quantity = total_quantity
                self.object.save()

                self.object.product.set(selected_products)

        return response

class OutflowDetail(DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflow'
