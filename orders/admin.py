from django.contrib import admin
from .models import Order, OrderItem, Table

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['table', 'paid', 'created']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number']
