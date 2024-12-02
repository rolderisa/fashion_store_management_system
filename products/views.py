from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Count,F
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import Product,  Category
from .forms import ProductForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

import logging
from django.db import transaction
from django.contrib import messages

from django.views.decorators.http import require_GET

@require_GET
def refresh_session(request):
    if request.user.is_authenticated:
        request.session.modified = True
    return JsonResponse({'status': 'ok'})
def product_list(request):
    # products = Product.objects.all()
    products=Product.objects.filter(user=request.user)

    return render(request, 'products/product_list.html', {'products': products})




@login_required
def add_product(request):
    
    if Category.objects.count() == 0:
        Category.objects.create(name="Men's Clothing", gender='M')
        Category.objects.create(name="Women's Clothing", gender='W')
        Category.objects.create(name="Accessories", gender='U')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

def storefront(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/storefront.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you want to redirect after editing
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

