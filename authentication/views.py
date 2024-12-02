from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Count,F
from django.utils import timezone
from datetime import timedelta
from django.db import models

from .forms import  UserRegisterForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
from django.db import transaction
from django.views.decorators.http import require_GET
from django.contrib.auth import login as auth_login
from django.utils import timezone

@require_GET
def refresh_session(request):
    if request.user.is_authenticated:
        request.session.modified = True
    return JsonResponse({'status': 'ok'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard/dashboard.html')
        else:
            return render(request, 'authentication/login.html',{'error':'Invalid credentials'})


    return render(request,'authentication/login.html')