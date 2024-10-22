from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import F 
from .models import BasketItem,WishItem
from shop.models import Product


def wishlist(request):
    return render(request, 'wishlist.html')

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            customer = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('customer:login')

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:home')
        return render(request, 'login.html', {'fail':True})
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('customer:login')

@login_required
def basket(request):
    basketList=request.user.customer.basketlist.all().annotate(total_price=F('count')*F('product__price'))
    return render(request,'basket.html',{
        'basketList':basketList
    })

from django.shortcuts import get_object_or_404

def add_basket(request, product_pk):
    if request.method == 'POST':
        size_pk = request.POST.get('size')
        color_pk = request.POST.get('color')
        count = request.POST.get('count')
        customer =request.user.customer

        existing_item = BasketItem.objects.filter(
            product_id=product_pk, size_id=size_pk, color_id=color_pk, customer=customer
        ).first()

        if existing_item:
            existing_item.count = F('count') + int(count)
            existing_item.save()                              
        else:                                                 
            BasketItem.objects.create(                        
                product_id=product_pk, size_id=size_pk, color_id=color_pk, count=count, customer=customer
            )

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('shop:home')
    
def increase_basket_item(request,basket_pk):
    basket=get_object_or_404(BasketItem,pk=basket_pk)
    basket.count=F('count')+1
    basket.save()
    return redirect('customer:basket')

def decrease_basket_item(request,basket_pk):
    basket=get_object_or_404(BasketItem,pk=basket_pk)
    if basket.count==1:
        basket.delete()
    else:
        basket.count=F('count')-1
        basket.save()                                         
    return redirect('customer:basket') 
                                                             
                                                                              
@login_required
def remove_basket(request,basket_pk):               
    basket=get_object_or_404(BasketItem,pk=basket_pk)      
    basket.delete()
    return redirect('customer:remove')                 

@login_required
def wish_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    customer=request.user.customer
    wishitem=WishItem.objects.filter(product=product,customer=customer).delete()
    return redirect(request.META.get('HTTP_REFERER'))                                              

@login_required                              
def unwish_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    customer=request.user.customer
    wishitem=WishItem.objects.create(product=product,customer=customer)
    return redirect(request.META.get('HTTP_REFERER'))
         
                     
          
