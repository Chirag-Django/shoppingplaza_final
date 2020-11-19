from django.db import models
from django.contrib.auth.models import User
from merchandise.models import Product
from django.db.models.signals import m2m_changed, pre_save

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=50,decimal_places=2,default=0.00)
    cart_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)


def subtotal_cart_reciever(sender, instance, action ,*args, **kwargs):
    if action == 'post_clear' or action == 'post_add' or action == 'post_remove':
        total = 0
        products = instance.products.all()
        for item in products:
            total += item.product_price
        instance.subtotal = total
        instance.save()

m2m_changed.connect(subtotal_cart_reciever, sender=Cart.products.through)


def total_cart_reciever(sender, instance,*args, **kwargs):
    instance.cart_total = instance.subtotal

pre_save.connect(total_cart_reciever, sender=Cart)
