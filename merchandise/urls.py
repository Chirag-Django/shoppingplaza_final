from django.urls import path
from . import views

app_name='merchandise'

urlpatterns = [
    path('home/',views.index,name='home'),
    path('products/',views.productList,name='products'),
    path('products/<slug>/',views.productDetails,name='product_details'),
]
