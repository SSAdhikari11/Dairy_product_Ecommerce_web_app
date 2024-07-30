from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart,Wishlist
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',{'totalitem':totalitem,'wishlistitem':wishlistitem})

@login_required
def contact(request):
    totalitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',{'totalitem':totalitem,'wishlistitem':wishlistitem})

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        context={'product':product,'title':title,'totalitem':totalitem,'wishlistitem':wishlistitem}
        return render(request, 'app/category.html',context)

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/category.html',locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request,pk):
        product=Product.objects.get(pk=pk)
        wishlist=Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        context={'product':product,'wishlist':wishlist,'totalitem':totalitem,'wishlistitem':wishlistitem}
        return render(request, 'app/productdetail.html',context)


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        context={'form':form}
        return render(request,'app/customerregistration.html',context)
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        context={'form':form}
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',context) 
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        context={'form':form,'totalitem':totalitem,'wishlistitem':wishlistitem}
        return render(request, 'app/profile.html',context)
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html')
    
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    context={'add':add,'totalitem':totalitem,'wishlistitem':wishlistitem}
    return render(request,'app/address.html',context)

@method_decorator(login_required,name='dispatch')
class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/updateaddress.html',context={'form':form,'totalitem':totalitem,'wishlistitem':wishlistitem})
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')
    
@login_required   
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount+=value
    totalamount=amount+40
    totalitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/showcart.html',{'cart':cart,'amount':amount,'totalamount':totalamount,'totalitem':totalitem,'wishlistitem':wishlistitem})


def plus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@method_decorator(login_required,name='dispatch')    
class Checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity*p.product.discounted_price
            famount+=value
        totalamount=famount+40
        totalitem=0
        wishlistitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlistitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/checkout.html',{'add':add, 'cart_items':cart_items,'totalamount':totalamount,'totalitem':totalitem,'wishlistitem':wishlistitem})


def plus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        Wishlist(user=request.user, product=product).save()
        data={
            'message':'Item added to wishlist Successfully'
        }
        return JsonResponse(data)
    

def minus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        Wishlist.objects.get(user=request.user, product=product).delete()
        data={
            'message':'Item deleted from wishlist Successfully'
        }
        return JsonResponse(data)
  

def show_wishlist(request):
    totalitem=0
    wishlistitem=0
    user=request.user
    if user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    product=Wishlist.objects.filter(user=user)
    context={'totalitem':totalitem,'wishlistitem':wishlistitem,'product':product}
    return render(request,'app/wishlist.html',context)

@login_required 
def search(request):
    query=request.GET['search']
    totalitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html',{'totalitem':totalitem,'wishlistitem':wishlistitem,'product':product})
