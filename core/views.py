
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, F
from . import metrics
import json


@login_required(login_url='login')
def home(request):
    period = int(request.GET.get('period', 7))

    company_user = getattr(request.user, 'profile', None)
    company = company_user.company if company_user else None

    product_metrics = metrics.get_product_metrics(company)
    sales_metrics = metrics.get_sales_metrics(company)
    daily_sales_data = metrics.get_daily_sales_data(period)
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data(period)
    graphic_product_category_metric = metrics.get_graphic_product_category_metric(company)
    graphic_product_brand_metric = metrics.get_graphic_product_brand_metric(company)

    # Calculando o valor total de vendas no período
    total_sales_value = sum(daily_sales_data['values'])

    # Calculando o número total de vendas no período (quantidade total de produtos vendidos)
    total_sales_quantity = sum(daily_sales_quantity_data['values'])

    context = {
        'product_metrics': product_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),
        'daily_sales_quantity_data': json.dumps(daily_sales_quantity_data),
        'product_count_by_category': json.dumps(graphic_product_category_metric),
        'product_count_by_brand': json.dumps(graphic_product_brand_metric),
        'current_period': period,
        'total_sales_value': total_sales_value,  # Valor total de vendas
        'total_sales_quantity': total_sales_quantity,  # Quantidade total de vendas
    }
    return render(request, 'home.html', context)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'profile'):
            return super().form_valid(form)  
        else:
            messages.error(self.request, "Este usuário não pertence a uma empresa.")
            return redirect('login')
