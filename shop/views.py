from django.shortcuts import render
from .models import Item, Category
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddItemForm
from cart.cart import Cart
from django.core.paginator import Paginator
import json

def item_list(request, table_id=None, category_slug=None):
    cart = Cart(request)
    category = None
    if table_id != None:
        if 'table_id' not in request.session:
            request.session['table_id'] = str(table_id)
    print(request.session['table_id'])
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    paginator = Paginator(items, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
        paginator = Paginator(items, 6) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    cart_items = []
    for i in cart:
        cart_items.append(i["item"].name)

    print(cart_items)
    cart_product_form = CartAddItemForm()
    return render(request,
                'list.html',
                {'category': category,
                'categories': categories,
                'items': items,
                'cart': cart,
                'cart_items': cart_items,
                'cart_product_form': cart_product_form,
                'page_obj': page_obj,
                'paginator': paginator
                })