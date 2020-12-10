from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('admin/', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('process/<int:order_id>', views.process_order, name='process_order'),
    path('process/table/<int:table_number>', views.process_table, name='process_table'),
]