from django.db import models
from cart_app.models import Cart
from address.models import ShippingAddress
from billing.models import BillingDetail
from .utils import unique_order_id_gen
from django.db.models.signals import pre_save, post_save
import decimal

# Create your models here.


ORDER_STATUS_CHOICES= (
    ('Not Yet Shipped', 'Not Yet Shipped'),
    ('Shipped', 'Shipped'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
    ('Paid','Paid')
    )

class Order(models.Model):
    order_id = models.CharField(max_length=200,unique=True,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    billing_details = models.ForeignKey(BillingDetail, on_delete=models.CASCADE,null=True,blank=True)
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,null=True,blank=True)
    order_status = models.CharField(max_length=120, default='Not Yet Shipped', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)

    def __str__(self):
        return self.order_id

    def change_total(self):
        self.total = decimal.Decimal(self.cart.cart_total) + decimal.Decimal(self.shipping_total)
        self.save()


def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_gen(instance)

pre_save.connect(pre_save_order_id, sender=Order)

def post_save_cart_total(sender, instance, *args, **kwargs):
    order_obj = Order.objects.filter(cart__id=instance.pk).first()
    if order_obj is not None:
        order_obj.change_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.change_total()

post_save.connect(post_save_order,sender=Order)