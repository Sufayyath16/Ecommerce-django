from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category


# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def checkout(request):
    return render(request,"checkout.html")

def payment(request):
    return render(request,"payment.html")



def product2(request):
    return render(request,"product2.html")

def single(request):
    return render(request,"single.html")

def single2(request):
    return render(request,"single2.html")
