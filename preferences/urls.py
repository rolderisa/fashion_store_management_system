from django.urls import path
from . import views

app_name = 'preferences'  

urlpatterns = [
  
    path('', views.customer_preference, name='customer_preference'),
    path('view/', views.view_preference, name='view_preference'),
    path('add/', views.add_preference, name='add_preference'),
    path('update/', views.update_preference, name='update_preference'),
   
]