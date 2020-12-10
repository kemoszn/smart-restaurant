from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import OrderItem, Order, Table

def order_list(request):
    orders = Order.objects.filter(processed=False)
    order_items = OrderItem.objects.all()
    tables = Table.objects.all()
    processed_orders = Order.objects.filter(processed=True, paid=False)
    return render(request, 'orders_list.html', {'orders': orders, 'order_items': order_items, 'tables': tables, 'proc_orders': processed_orders })

def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        if 'table_id' in request.session:
            table_id = request.session['table_id']
        order = Order.objects.create(table=table_id, total=cart.get_total_price(), paid=False)
        for item in cart:
            OrderItem.objects.create(order=order,
                            item=item['item'],
                            price=item['price'],
                            quantity=item['quantity'])
        cart.clear()
        return render(request,
                    'created.html',
                    {'order': order})
    else:
        return render(request,
                'create.html',
                {'cart': cart})
            

def process_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items: 
        print(item.item)
    Order.objects.filter(id=order_id).update(processed=True)
    return redirect(request.META['HTTP_REFERER'])

def process_table(request, table_number):
    table = get_object_or_404(Table, number=table_number)
    Order.objects.filter(table=table.number).update(paid=True)
    print("Hello?")

    return redirect(request.META['HTTP_REFERER'])
