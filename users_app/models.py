from django.db import models

# Create your models here.
class GuestCustomer(models.Model):
    email = models.EmailField()
    name = models.CharField(default="Happy Guest",max_length=50)
    guest_created = models.DateTimeField(auto_now_add=True)
    guest_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email