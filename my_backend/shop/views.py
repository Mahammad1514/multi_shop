from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.db.models import Count,Avg
from .models import Campaign,Category,Product,Size,Color,Contact 
from customer.models import Review
from .filters import ProductFilter
from .forms import ContactForm
from django.core.paginator import Paginator,EmptyPage
# import requests
# import json 
# Create your views here.     

def home(request):
    slide_campaigns=Campaign.objects.filter(is_slide=True)[:3]
    nonslide_campaigns=Campaign.objects.filter(is_slide=False)[:4]
    categories=Category.objects.annotate(product_count=Count('products'))
    featured_products=Product.objects.filter(featured=True)[:8]
    recent_products=Product.objects.all().order_by('-created')[:8]
    return render(request, 'home.html',{
        'slide_campaigns':slide_campaigns,
        'nonslide_campaigns':nonslide_campaigns,
        'categories':categories,
        'featured_products':featured_products,
        'recent_products':recent_products,

    })

def product_list(request):
    products=Product.objects.all().annotate(avg_star=Avg('reviews__star_count'))
    search_input=request.GET.get('search')

    if search_input:
        product=request.filter(title__icontains=search_input)

    sorting_input=request.GET.get('sorting')   
    if sorting_input:
        products=products.order_by(sorting_input)

    product_filter=ProductFilter(request.GET, queryset=products)
    # products=product_filter.qs 

    page_by_input=int(request.GET.get('page_by', 3))
    # page_input=int(request.get.get('page', 1))
    paginator=Paginator(products, page_by_input) 

    # try:
        # page=paginator.page(page_input)
        # products=page.object_list

    # except EmptyPage:
        # page=paginator.page(1)
        # products=page.object_list

    colors=Color.objects.all().annotate(product_count=Count('products'))
    sizes=Size.objects.all().annotate(product_count=Count('products'))    

    return render(request, 'product-list.html', {
        'products':products,
        'paginator':paginator,
        # 'page':page,                                                                          
        'sizes':sizes,
        'colors':colors,
    })

    colors = Color.objects.all().annotate(product_count=Count('products'))
    sizes = Size.objects.all().annotate(product_count=Count('products'))
    
    product = Product.objects.all()
    return render(request, 'product-list.html', {
        "products": product,

    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    other_products = Product.objects.exclude(pk=product.pk).order_by('?')[:5]
    has_review=has_review = Review.objects.filter(customer=request.user.customer, product=product).exists()
    return render(request, 'product-detail.html', {
        'product': product,
        'other_products': other_products,
    })


def contact(request):
    form=ContactForm()
    if request.method=='POST':
        recaptcha_response = request.POST.get('g-recaptcha-response') 
        response = request.POST.get('https://www.google.com/recaptcha/api/siteverify',{
            'secret':'6LfijC0qAAAAAIJpRtN5Jb47EaK8HfkqTAWQa9um',
            'response':recaptcha_response,
        })  
        response_data=response.json()
        form=ContactForm(request.POST)
        if form.is_valid() and response_data['success'] and response_data['score'] > 0.7:  
            form.save()
            return render(request,'contact.html',{'form':form,'result':'success'})
        return render(request,'contact.html',{'form':form,'result':'fail'})
    return render(request,'contact.html',{'form':form}) 


def confirm_contact(request):
    if request.method=='GET':
        return redirect('shop:contact')
    elif request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        contact=Contact(name=name,email=email,phone=phone,message=message)
        contact.save()
        return redirect('shop:contact')
    
def review(request, pk):
    if request.method == 'POST':
        customer = request.user.customer
        product = get_object_or_404(Product, pk=pk)
        if Review.objects.filter(customer=customer, product=product).exists():
            return HttpResponse(status=403)
        star_count = int(request.POST.get('star_count'))
        comment = request.POST.get('comment')
        Review.objects.create(
            customer=customer, product=product,
            comment=comment, star_count=star_count
        )
        return redirect('shop:product-detail', pk=pk)
    return redirect('shop:product-detail', pk=pk)



    