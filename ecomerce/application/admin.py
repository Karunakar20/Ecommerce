from django.contrib import admin
from . models import Products, Customer, Wishlist, Cart, CartItem


# Register your models here.
@admin.register(Products)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','zipcode', 'state']


admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)