from django.shortcuts import render, render_to_response
from .models import Item, Category
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddItemForm
from cart.cart import Cart
from django.core.paginator import Paginator
import json
from django.template import RequestContext

def handler500(request):
    data = {}
    return render(request, '505.html', data)


def item_list(request, table_id=None, category_slug=None):
    cart = Cart(request)
    category = None
    if table_id != None:
        if 'table_id' not in request.session:
            request.session['table_id'] = str(table_id)
    #print(request.session['table_id'])
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


def take_out(request, category_slug=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    
    cart_items = []
    for i in cart:
        cart_items.append(i["item"].name)
    cart_product_form = CartAddItemForm()
    return render(request, 'takeout.html', {'category': category,
                                             'items': items,
                                             'cart_items': cart_items, 
                                             'cart': cart,
                                             'categories': categories,
                                             'cart_product_form': cart_product_form})
