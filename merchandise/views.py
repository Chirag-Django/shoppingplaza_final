from django.shortcuts import render
from .models import Product
from django.http import Http404
from cart_app.models import Cart

# Create your views here.

def index(request):
    featured_products = Product.objects.all().filter(featured_item=True)[:3]
    return render(request,'merchandise/index.html', {'featured_products':featured_products})

def productList(request):
    products = Product.objects.all()

    common_tags = Product.product_tags.most_common()[:4]
    return render(request,'merchandise/all_products.html',{'all_products':products,'common_tags':common_tags,
                                                           })

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


