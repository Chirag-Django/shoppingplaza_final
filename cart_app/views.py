from django.shortcuts import render, redirect
from .models import Cart
from merchandise.models import Product
from orders.models import Order
from billing.models import BillingDetail
from users_app.models import GuestCustomer
from address.forms import ShippingAddressForm
from address.models import ShippingAddress
from django.http import JsonResponse

# Create your views here.

def get_or_create_cart(request):
    global my_cart
    global new_cart
    cart_pk = request.session.get('cart_pk',None)
    user = request.user
    if cart_pk is None:
        new_cart = True
        if user.is_anonymous:
            my_cart = Cart.objects.create(user=None)
        elif user.is_authenticated:
            my_cart = Cart.objects.create(user=user)
        request.session['cart_pk'] = my_cart.pk
    else:
        new_cart = False
        my_cart = Cart.objects.filter(pk=cart_pk).first()
        if user.is_authenticated and my_cart.user is None:
            my_cart.user = request.user
            my_cart.save()
    return new_cart,my_cart

def cart_index(request):
    new_cart, my_cart = get_or_create_cart(request)
    request.session['item_count'] = my_cart.products.count()
    return render(request,'cart_app/cart_main.html',{'my_cart':my_cart})

def cart_add(request):
    productId = request.POST.get('productId')
    product_added = False
    new_cart, my_cart = get_or_create_cart(request)
    if productId:
        try:
            product = Product.objects.get(id=productId)
        except Product.DoesNotExist:
            return redirect('cart_app:cart')
        my_cart.products.add(product)
        product_added = True
    request.session['item_count'] = my_cart.products.count()
    if request.is_ajax():
        jsonData = {
            'product_added' : product_added,
            'product_removed': not product_added,
            'cartItemCount': my_cart.products.count()
        }
        return JsonResponse(jsonData)
    return redirect('cart_app:cart')

def cart_remove(request):
    productId = request.POST.get('productId')
    new_cart, my_cart = get_or_create_cart(request)
    product = Product.objects.get(id=productId)
    my_cart.products.remove(product)
    return redirect('cart_app:cart')

def checkout_page(request):
    new_cart, my_cart = get_or_create_cart(request)
    user = request.user
    billing_details = None
    my_order = None
    guest_email = request.session.get('guest_email')
    if not new_cart:
        my_order,created = Order.objects.get_or_create(cart=my_cart)
    elif my_cart.products.count()==0:
        return redirect('cart_app:cart')
    if user.is_authenticated:
        if guest_email:
            del request.session['guest_email']
        billing_details, created = BillingDetail.objects.get_or_create(billing_user=user,billing_email=user.email)
    elif guest_email:
        guest_registered = GuestCustomer.objects.filter(email=guest_email).first()
        billing_details, created = BillingDetail.objects.get_or_create(billing_email=guest_registered.email)
    form = ShippingAddressForm()
    if request.method == 'POST':
        form = ShippingAddressForm(data=request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.billing_details = billing_details
            form.save()
            request.session['shipping_addr_id'] = form.pk
    shipping_addr_id = request.session.get('shipping_addr_id')
    shipping_object = ShippingAddress.objects.filter(id=shipping_addr_id).first()
    if my_order:
        my_order.billing_details = billing_details
        my_order.shipping_address = shipping_object
        my_order.save()
    return render(request,'cart_app/checkout_page.html',{'my_order':my_order,
                                                         'billing_details':billing_details,
                                                         'shipping_address':form,'shipping_object':shipping_object})

def confirm_order(request):
    new_cart, my_cart = get_or_create_cart(request)
    guest_email = request.session.get('guest_email')
    shipping_addr_id = request.session.get('shipping_addr_id')
    if not new_cart:
        my_order,created = Order.objects.get_or_create(cart=my_cart)
        my_order.order_status = 'Shipped'
        del request.session['cart_pk']
        if guest_email:
            del request.session['guest_email']
        if shipping_addr_id:
            del request.session['shipping_addr_id']
        request.session['item_count'] = 0
        my_order.save()
        return render(request,'cart_app/confirm_order.html')
    elif new_cart or my_cart.products.count()==0:
        return redirect('cart_app:cart')


