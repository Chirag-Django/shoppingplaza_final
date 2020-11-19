from django.db import models
from django.contrib.auth.models import User
from billing.models import BillingDetail

# Create your models here.
class Address(models.Model):
    billing_details = models.ForeignKey(BillingDetail,on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=300)
    line_2 = models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=150)

    class Meta:
        abstract = True



class ShippingAddress(Address):
    def __str__(self):
        return 'Shipping Address :'+ str(self.billing_details)

    class Meta:
        verbose_name_plural = "Shipping Addresses"

# class BillingAddress(Address):
#     def __str__(self):
#         return 'Billing Address :'+ str(self.billing_details)
#
#     class Meta:
#         verbose_name_plural = "Billing Addresses"