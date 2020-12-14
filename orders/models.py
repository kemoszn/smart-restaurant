from django.db import models
from shop.models import Item
from django.db.models import signals
from django.dispatch import receiver
from webpush import send_user_notification 
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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

@receiver(signals.post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    print("order created")
    user = get_object_or_404(User, pk=1)
    print(user)
    payload = {"head": "Welcome!", "body": "Hello World"}
    send_user_notification(user=user, payload=payload, ttl=1000)


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