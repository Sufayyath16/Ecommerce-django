from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product, Variation
from carts.models import Cart
from carts.models import CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

#The use of the session for storing the cart_id allows the application to associate a user's cart with their session, even if they are not authenticated.
#This is useful in scenarios where users can add items to their cart before creating an account or logging in.
#The cart_id is a key identifier associated with a user's shopping cart. It helps the application keep track of which cart belongs to which user.

def _cart_id(request):
    cart = request.session.session_key #attempts to retrieve the existing cart_id from the session.
    if not cart:
        cart = request.session.create()  #If there is no existing session key (if not cart), a new session is created using request.session.create().
    return cart



#try and except blocks are used to gracefully handle the situation where the specified Cart object is not found in the database. Instead of crashing the application with an unhandled exception, it allows the code to proceed without displaying an error to the user.

def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass  
        
        


        
        
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            


            if product_variation in ex_var_list:
            #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)

                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('/cart/')
    # if the user is not authenticated

    else:
        
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass  
        
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart-id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        
        
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)



            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)


            if product_variation in ex_var_list:
            #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)

                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('/cart/')

# to decrement quantity of cart items
def remove_cart(request,product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
       if request.user.is_authenticated:
          cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
       else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
       if cart_item.quantity > 1:
          cart_item.quantity -= 1
          cart_item.save()
       else:
        cart_item.delete()
    except:
        pass
    return redirect('/cart/')

#to delete item from cart
def remove_cart_item(request,product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
       cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
       cart = Cart.objects.get(cart_id=_cart_id(request))

       cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('/cart/')
    



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  #just ignore


    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request,'cart.html',context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  #just ignore


    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'checkout.html', context)
