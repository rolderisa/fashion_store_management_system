from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Count,F
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product,Cart,CartItem
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.views.decorators.http import require_POST
import logging
from django.db import transaction

from django.views.decorators.http import require_GET

@require_GET
def refresh_session(request):
    if request.user.is_authenticated:
        request.session.modified = True
    return JsonResponse({'status': 'ok'})

logger = logging.getLogger(__name__)


@require_POST
@login_required
def add_to_cart(request, product_id):
    try:
        with transaction.atomic():
            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            cart_count = sum(item.quantity for item in cart.cartitem_set.all())

            return JsonResponse({
                'status': 'success',
                'message': 'Product added to cart successfully',
                'cart_count': cart_count
            })
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
# @login_required
# def view_cart(request):
#     cart,created=Cart.objects.get_or_create(user=request.user)
#     items=cart.items.all()
#     total=sum(item.product.price * item.quantity for item in items)
#     return render(request, 'store/cart.html',{'items':items,'total':total})    
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'cart/view_cart.html', context)