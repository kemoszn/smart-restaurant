from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:table_id>', views.item_list, name='item_list_by_table'),
    path('<slug:category_slug>/', views.item_list,
    name='item_list_by_category'),
]