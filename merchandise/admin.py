from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','product_slug','product_price','product_active','featured_item','product_tags']

admin.site.register(Product, ProductAdmin)