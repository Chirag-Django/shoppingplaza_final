from django.shortcuts import render
from .models import Product
from django.http import Http404
from cart_app.models import Cart
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

def index(request):
    featured_products = Product.objects.all().filter(featured_item=True)[:3]
    return render(request,'merchandise/index.html', {'featured_products':featured_products})

def productList(request):
    products = Product.objects.all()
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
    return render(request,'merchandise/all_products.html',{'all_products':products,'page_product':page_product})


def productList_Category_Wise(request,product_category=None):
    products = Product.objects.all().filter(product_category=product_category)
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
    return render(request,'merchandise/all_products.html',{'all_products':products,'page_product':page_product,"product_category":product_category})


def productDetails(request,slug=None):
    global product_details
    global message
    try:
        product_details = Product.objects.get(product_slug=slug)
        message = None
        if product_details is None:
            message = "Product Not Found"
    except Product.DoesNotExist:
        raise Http404("Product Doesnot Exists")
    cart_pk = request.session.get('cart_pk', None)
    cart = Cart.objects.filter(pk=cart_pk).first()
    return render(request,'merchandise/product_details.html',{'product_details': product_details,
                                                              'message': message,
                                                              'cart':cart})


def customer_care(request):
    return render(request,'merchandise/customer_care.html')