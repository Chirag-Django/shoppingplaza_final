from django.db import models
from random import randint
import os
from django.dispatch import receiver
from .slugGenerator import unique_slug_generator
from taggit.managers import TaggableManager

# Create your models here.

def file_extention(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image(instance, filename):
    new_filename = randint(0,100000000)
    name, ext = file_extention(filename)
    final_filename = f'{new_filename}{ext}'
    return f'merchandise/{new_filename}/{final_filename}'


class CustomProductManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Product(models.Model):
    product_name = models.CharField(max_length=256)
    product_details = models.TextField()
    product_price = models.DecimalField(max_digits=19, decimal_places=2,default=0.00)
    product_image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    product_slug = models.SlugField(unique=True, null=True, blank=True)
    product_tags = TaggableManager(blank=True)
    product_active = models.BooleanField(default=True)
    featured_item = models.BooleanField(default=False)
    product_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CustomProductManager()

    def get_absolute_url(self):
        return "{slug}/".format(slug=self.product_slug)

    def __str__(self):
        return self.product_name

@receiver(models.signals.pre_save, sender=Product)
def auto_slug_generator(sender, instance, **kwargs):
    if not instance.product_slug:
        instance.product_slug = unique_slug_generator(instance)