from django.urls import path
from . import views

urlpatterns = [
    path('', views.storefront, name='storefront'),
    path('add/', views.add_product, name='add_product'),
    path('refresh-session/', views.refresh_session, name='refresh_session'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/', views.product_list, name='product_list'),
    
]
