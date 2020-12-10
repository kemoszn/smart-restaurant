from django.db import models
from shop.models import Item

class Table(models.Model):
    number = models.IntegerField()

    class Meta: 
        ordering = ('-number',)

    def __str__(self):
        return str(self.number)


class Order(models.Model):
    table = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                    related_name='items',
                    on_delete=models.CASCADE)
    item = models.ForeignKey(Item,
                    related_name='order_items',
                    on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity