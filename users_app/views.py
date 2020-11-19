from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CustomRegisterForm,CustomGuestRegisterForm
from .models import GuestCustomer

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = CustomRegisterForm(request.POST,None)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,("New User Account Created Sucessfully!"))
            return redirect('merchandise:products')
    else:
        register_form = CustomRegisterForm()
    return render(request,'register.html',{'register_form': register_form})

def guest_register(request):
    if request.method == 'POST':
        custom_register_form = CustomGuestRegisterForm(request.POST)
        if custom_register_form.is_valid():
            guest_email = request.POST.get('email')
            custom_register_form.save()
            messages.success(request,("Guest Account Created Sucessfully!Start Shopping"))
            guest_registered = GuestCustomer.objects.filter(email=guest_email).first()
            request.session['guest_email'] = guest_registered.email
            return redirect('merchandise:products')
    else:
        custom_register_form = CustomGuestRegisterForm()
    return render(request,'register.html',{'register_form': custom_register_form})