from django.urls import path
from . import views

urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    path('add/', views.add_sale, name='add_sale'),
    path('delete/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('view/<int:sale_id>/', views.view_sale, name='view_sale'),
    path('edit/<int:sale_id>/', views.edit_sale, name='edit_sale'),
    path('refresh-session/', views.refresh_session, name='refresh_session'),
    
]