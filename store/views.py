from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

# to display products in store and also display it category wise
def product(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:         #to display products category wise
        categories = get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,6)
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6) #pagination->6 products should display in 1 page
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
    }
    return render(request,"product.html",context)

# single product view
def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        
    }
    return render(request,'single.html',context)


# search in navbar
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            #get the product by its description or name
    context = {
        'products': products,
    }
    return render(request,'product.html',context)



