from django.urls import path
from . import views

app_name='merchandise'

urlpatterns = [
    path('home/',views.index,name='home'),
    path('products/',views.productList,name='products'),
    path('products/<product_category>',views.productList_Category_Wise,name='products_category'),
    path('products/<slug>/',views.productDetails,name='product_details'),
    path('customer_care/',views.customer_care,name='customer_care')
]
