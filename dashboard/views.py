from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from products.models import Product
from sales.models import Sale

@login_required
def dashboard(request):
    user_products = Product.objects.filter(user=request.user)
    user_sales = Sale.objects.filter(user=request.user)
    
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    total_sales = user_sales.filter(date__gte=last_30_days).aggregate(
        total=Sum('total_price'))['total'] or 0
    
    sales_by_category = user_sales.filter(date__gte=last_30_days).values(
        'product__category__name').annotate(
        total=Sum('total_price')).order_by('-total')
    
    low_stock_products = user_products.filter(stock__lte=F('low_stock_threshold'))

    # Fetch sales data for the last 6 months
    six_months_ago = today - timedelta(days=180)
    sales_data = user_sales.filter(date__gte=six_months_ago).values('date__month', 'date__year').annotate(
        total=Sum('total_price')).order_by('date__year', 'date__month')

    # Prepare data for the chart
    labels = []
    data = []
    for entry in sales_data:
        month_name = timezone.datetime(year=entry['date__year'], month=entry['date__month'], day=1).strftime('%b')
        labels.append(month_name)
        data.append(float(entry['total']))

    context = {
        'total_sales': total_sales,
        'sales_by_category': sales_by_category,
        'low_stock_products': low_stock_products,
        'products': user_products,
        'sales': user_sales,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'dashboard/dashboard.html', context)