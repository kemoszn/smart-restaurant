from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import OrderItem, Order, Table

def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(processed=False)
        order_items = OrderItem.objects.all()
        tables = Table.objects.all()
        processed_orders = Order.objects.filter(processed=True, paid=False)
        active_tables = []
        for order in processed_orders:
            if order.table not in active_tables:
                active_tables.append(order.table)
        return render(request, 'orders_list.html', {'orders': orders, 'order_items': order_items, 'tables': active_tables, 'proc_orders': processed_orders })


def create_order(request):
    cart = Cart(request)
    if (request.user_agent.is_mobile or request.user_agent.is_tablet) and cart.__len__() > 0:
        if request.method == 'POST':
            if 'table_id' in request.session:
                table_id = request.session['table_id']
            else:
                return render(request, 'please.html')
            order = Order.objects.create(table=table_id, total=cart.get_total_price(), paid=False)
            for item in cart:
                OrderItem.objects.create(order=order,
                                item=item['item'],
                                price=item['price'],
                                quantity=item['quantity'])
            del request.session['table_id']
            request.session.modified = True                    
            cart.clear()
            return render(request,
                        'created.html',
                        {'order': order})
        else:
            return render(request,
                    'create.html',
                    {'cart': cart})
    else:
        return render(request, 
                    'please.html')
            
def process_order(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        print(order)
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items: 
            print(item.item)
        Order.objects.filter(id=order_id).update(processed=True)
        return redirect(request.META['HTTP_REFERER'])


def process_table(request, table_number):
    if request.user.is_superuser:
        table = get_object_or_404(Table, number=table_number)
        orders = Order.objects.filter(table=table.number, processed=True, paid=False)
        order_items = OrderItem.objects.all()
        total = 0
        for order in orders: 
            for item in order_items:
                if item.order == order:
                    print(str(item.item)+' '+ str(item.quantity)+ ' ' + str(item.quantity*item.price))
                    total = total + (item.price*item.quantity)
        print("Total: " + str(total) + "SDG")
        #Order.objects.filter(table=table.number, processed=True).update(paid=True)

        return redirect(request.META['HTTP_REFERER'])


def create_order_admin(request):
    if request.user.is_superuser:
        cart = Cart(request)
        for item in cart:
            print(str(item['item']) + ' ' + str(item['quantity']) + ' ' + str(item['price']))
        print(cart.get_total_price())
        cart.clear()
        return redirect('shop:take_out')
