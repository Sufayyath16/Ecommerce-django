from django.shortcuts import render,get_object_or_404
from store.models import Product, ReviewRating
from category.models import Category


# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True).order_by('created_date')

    # get the reviews
    for product in products:
       reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    
    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")



def help(request):
    return render(request,"help.html")

def faqs(request):
    return render(request,"faqs.html")

def terms(request):
    return render(request,"terms.html")

def privacy(request):
    return render(request,"privacy.html")












