from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class BillingDetail(models.Model):
    billing_user = models.OneToOneField(User,blank=True,null=True, unique=True,on_delete=models.CASCADE)
    billing_email = models.EmailField()
    billing_created_at = models.DateTimeField(auto_now_add=True)
    billing_modified_at = models.DateTimeField(auto_now=True)
    billing_active = models.BooleanField(default=True)

    def __str__(self):
        return self.billing_email

def associate_user(sender, instance, created, *args, **kwargs):
    if created:
        BillingDetail.objects.create(billing_user=instance,billing_email=instance.email)

post_save.connect(associate_user, sender=User)


