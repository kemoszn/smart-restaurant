from decimal import Decimal
from django.conf import settings
from shop.models import Item

class Cart(object):

    def __init__(self, request):
        #initialize the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    
    def add(self, item, quantity=1, update_quantity=False):
        """
        Add a item to the cart or update its quantity.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                'price': str(item.price)}
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()


    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, item):
        """
        Remove a item from the cart.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the items
        from the database.
        """
        item_ids = self.cart.keys()
        # get the item objects and add them to the cart
        items = Item.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]['item'] = item

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()