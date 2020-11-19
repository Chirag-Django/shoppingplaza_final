from django.shortcuts import render
from django.views.generic import ListView
from merchandise.models import Product
from django.db.models import Q
from taggit.models import Tag


# Create your views here.
def searchProduct(request):
    search_product = request.GET.get('search')
    if search_product:
        products = Product.objects.filter(Q(product_name__icontains=search_product)
                                          | Q(product_details__icontains=search_product)
                                          | Q(product_tags__name__in=[search_product,])).distinct()
    else:
        products = Product.objects.none()
    return render(request,'merchandise/all_products.html',{'all_products':products,'search_product':search_product})
