from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'orders'

urlpatterns = [
    path('admin/', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('process/<int:order_id>', views.process_order, name='process_order'),
    path('process/table/<int:table_number>', views.process_table, name='process_table'),
    path('takeout/process', views.create_order_admin, name='create_order_admin'),
]