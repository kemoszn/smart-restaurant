from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Item)
class ItemADmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'category', 'price', 'available']
    list_filter = ['available']
