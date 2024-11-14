from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from . models import Customer, Products, Wishlist, Cart, CartItem
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_page(request):
    data = Products.objects.all()
    contex = {'data': data}
    return render(request,'app/home.html', contex)


class CategoryView(View):
    def get(self,request,val):
        products = Products.objects.filter(category=val)
        titles = products.values('title')
        return render(request, 'app/category.html', {'products': products, 'titles': titles})
    

class ProductDetail(View):
    def get(self,request,pk):
        product = Products.objects.get(pk=pk)
        return render(request,'app/productdeatils.html',{'product': product})
    
def about_page(request):
    return render(request,'app/about.html')

def contact_page(request):
    return render(request,'app/contact.html')

class CustomerRegistration(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,"app/customerregistration.html",locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Register Sucessfully !")

        else:
            messages.warning(request,"Registration is failed !")

        return render(request,"app/customerregistration.html",locals()) 

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"app/profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Profile Created Sucessfully !")
        
        else:
            messages.warning(request,"Profile Creation is failed !")

        return render(request,"app/profile.html",locals())
    
def Logout(request):
    logout(request)
    return redirect('home')

#wishlist

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Products, id=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, f'{product.title} was added to your wishlist.')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Products, id=pk)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    messages.success(request, f'{product.title} was removed from your wishlist.')
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    context = {
        'wishlist': wishlist.products.all()
    }
    return render(request, 'app/wishlist.html', context)

#cart

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'app/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Products, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.title} was added to your cart.')
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
    cart_item.delete()
    messages.success(request, 'Item was removed from your cart.')
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart_items = CartItem.objects.all()
    address = Customer.objects.all()
   
    return render(request,'app/checkout.html',locals())

@login_required
def Order_placed(request):
    return render(request,'app/orderplace.html')

def Address(request):
    address = Customer.objects.all()
    return render(request,'app/address.html',locals())