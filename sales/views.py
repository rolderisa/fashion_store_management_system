from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from django.db import models, transaction
from .models import Sale
from .forms import SaleForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
import logging

@require_GET
def refresh_session(request):
    if request.user.is_authenticated:
        request.session.modified = True
    return JsonResponse({'status': 'ok'})

@login_required
def sale_list(request):
    sales = Sale.objects.filter(user=request.user)
    return render(request, 'sales/sale_list.html', {'sales': sales})

@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            
            
            product = sale.product
            product.stock -= sale.quantity
            product.save()
            
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/add_sale.html', {'form': form})

@login_required
@require_http_methods(["DELETE"])
def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    with transaction.atomic():
      
        product = sale.product
        product.stock += sale.quantity
        product.save()
        
        sale.delete()
    return JsonResponse({"message": "Sale deleted successfully"}, status=200)

@login_required
@require_GET
def view_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    data = {
        'id': sale.id,
        'product': {'name': sale.product.name},
        'quantity': sale.quantity,
        'total_price': str(sale.total_price),
        'date': sale.date.isoformat()
    }
    return JsonResponse(data)

@login_required
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            with transaction.atomic():
              
                old_product = sale.product
                old_product.stock += sale.quantity
                old_product.save()
                
                
                updated_sale = form.save()
                
               
                new_product = updated_sale.product
                new_product.stock -= updated_sale.quantity
                new_product.save()
            
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'sales/edit_sale.html', {'form': form, 'sale': sale})