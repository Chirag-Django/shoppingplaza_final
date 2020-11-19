from django.contrib import admin
from .models import BillingDetail

# Register your models here.
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = ['billing_user','billing_email','billing_active']

admin.site.register(BillingDetail,BillingDetailsAdmin)