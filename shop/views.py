from django.shortcuts import render
from .models import Item, Category
from django.shortcuts import render, get_object_or_404


def item_list(request, category_slug=None):
    category = None
    print(category_slug)
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    
    return render(request,
                'list.html',
                {'category': category,
                'categories': categories,
                'items': items})