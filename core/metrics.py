from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, F
from django.utils.formats import number_format
from products.models import Product
from outflows.models import Outflow
from brands.models import Brand
from categories.models import Category
from serviceprovision.models import ServiceProvision

def get_product_metrics(company):
    products = Product.objects.filter(company=company)

    total_cost_price = sum(product.cost_price * product.quantity for product in products)
    total_selling_price = sum(product.selling_price * product.quantity for product in products)
    total_quantity = sum(product.quantity for product in products)
    total_profit = total_selling_price - total_cost_price

    return dict(
        total_cost_price=number_format(total_cost_price, decimal_pos=2, force_grouping=True),
        total_selling_price=number_format(total_selling_price, decimal_pos=2, force_grouping=True),
        total_quantity=total_quantity,
        total_profit=number_format(total_profit, decimal_pos=2, force_grouping=True),
    )

def get_sales_metrics(company):
    outflows = Outflow.objects.filter(company=company)

    total_products_sold = outflows.aggregate(
        total_products_sold=Sum('quantity')
    )['total_products_sold'] or 0

    total_sales = outflows.count()

    total_sales_value = sum(
        sum(product.selling_price * outflow.quantity for product in outflow.product.all())
        for outflow in outflows
    )

    total_sales_cost = sum(
        sum(product.cost_price * outflow.quantity for product in outflow.product.all())
        for outflow in outflows
    )

    total_sales_profit = total_sales_value - total_sales_cost

    return dict(
        total_sales=total_sales,
        total_products_sold=total_products_sold,
        total_sales_value=number_format(total_sales_value, decimal_pos=2, force_grouping=True),
        total_sales_profit=number_format(total_sales_profit, decimal_pos=2, force_grouping=True),
    )

def get_daily_sales_data(company, period=7):
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(period - 1, -1, -1)]  
    values = list()

    for date in dates:
        sales_total = Outflow.objects.filter(
            company=company,
            created_at__date=date
        ).aggregate(
            total_sales=Sum(F('product__selling_price') * F('quantity'))
        )['total_sales'] or 0
        values.append(float(sales_total))

    return dict(
        dates=dates,  
        values=values
    )

def get_daily_sales_quantity_data(company, period=7):
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(period - 1, -1, -1)]
    quantities = list()

    for date in dates:
        sales_quantity = Outflow.objects.filter(
            company=company,
            created_at__date=date
        ).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
        quantities.append(sales_quantity)
    
    return dict(
        dates=dates,
        values=quantities
    )

def get_graphic_product_category_metric(company):
    categories = Category.objects.all()
    return {category.name: Product.objects.filter(category=category, company=company).count() for category in categories}

def get_graphic_product_brand_metric(company):
    brands = Brand.objects.all()
    return {brand.name: Product.objects.filter(brand=brand, company=company).count() for brand in brands}

def get_service_metrics(company):
    services = ServiceProvision.objects.filter(company=company)

    total_services_provisioned = services.aggregate(
        total_services_provisioned=Sum('quantity')
    )['total_services_provisioned'] or 0

    total_services = services.count()

    total_services_value = sum(
        sum(service_provision.value * service.quantity for service_provision in ServiceProvision.service.all())
        for service in services
    )

    total_services_cost = sum(
        sum(service_provision.cost_price * service.quantity for service_provision in ServiceProvision.service.all())
        for service in services
    )

    total_services_profit = total_services_value - total_services_cost

    return dict(
        total_services=total_services,
        total_services_provisioned=total_services_provisioned,
        total_services_value=number_format(total_services_value, decimal_pos=2, force_grouping=True),
        total_services_profit=number_format(total_services_profit, decimal_pos=2, force_grouping=True),
    )
