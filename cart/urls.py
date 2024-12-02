from django.urls import path
from . import views

urlpatterns = [
    # path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
      path('', views.view_cart, name='view_cart'),
     path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    path('refresh-session/', views.refresh_session, name='refresh_session'),
]
