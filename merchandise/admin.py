from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','product_category','product_slug','product_price','product_rating','product_active','product_tags']

admin.site.register(Product, ProductAdmin)