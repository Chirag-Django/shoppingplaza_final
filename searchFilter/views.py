from django.shortcuts import render
from django.views.generic import ListView
from merchandise.models import Product
from django.db.models import Q
from taggit.models import Tag
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
def searchProduct(request):
    search_product = request.GET.get('search')
    if search_product:
        products = Product.objects.filter(Q(product_name__icontains=search_product)
                                          | Q(product_details__icontains=search_product)
                                          | Q(product_tags__name__in=[search_product,])).distinct()
    else:
        products = Product.objects.none()
    if request.method == 'POST':
        selected_sort = request.POST.get('selected_sort')
        if selected_sort == 'lowToHigh':
            products = products.order_by('product_price')
        elif selected_sort == 'highToLow':
            products = products.order_by('-product_price')
        elif selected_sort == 'ratingLowToHigh':
            products = products.order_by('product_rating')
        elif selected_sort == 'ratingHighToLow':
            products = products.order_by('-product_rating')
    page_product = products
    page = request.GET.get('page', 1)
    paginator = Paginator(page_product, 8)
    try:
        page_product = paginator.page(page)
    except PageNotAnInteger:
        page_product = paginator.page(1)
    except EmptyPage:
        page_product = paginator.page(paginator.num_pages)
    return render(request,'merchandise/all_products.html',{'all_products':products,'search_product':search_product,
                                                           'page_product':page_product})
