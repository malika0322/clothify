import hashlib
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
# from .forms import ContactForm  # Import the form class (we'll create this next)
from datetime import datetime
import time

import requests
from home.models import Contact
from django.contrib import messages
from .models import*
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product


#from .models import Cart

# Create your views here.


# def upload_page(request):
#     return render(request,'upload.html')

def index(request):
    products=Product.objects.all()
    
    # return HttpResponse("this is home page.")
    if request.GET.get('search'):
        products= products.filter(product_name__icontains = request.GET.get('search'))
        search=True
    else:
        search=False
    context = {
        'products' : products,
        'search' : search
    }

    return render(request,'index.html',context)
 
def aboutus(request):
    return render(request,'aboutus.html')
    # return HttpResponse("this is about page.")



def shop(request,option_name):
    products=Product.objects.filter(category__name__icontains=option_name)
    context = {
        'products' : products
    }
    return render(request,'shop.html',context)
    # return HttpResponse("this is service page.")

# def contact(request):
#     return render(request,'contact.html')
#     # return HttpResponse("this is contact page.")



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Use the correct model (e.g., 'Contact' with an uppercase C)
        contact = Contact(name=name, email=email, message=message, date=datetime.today())
        contact.save()
        messages.success(request, f"Thank you, {name}. We have received your message")
        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')

def product_overview(request,id):
    products = Product.objects.get(id=id)
    context = {
        'products' : products
    }
    return render(request,'overview.html',context)


def faqs(request):
    return render(request, 'faqs.html')

def policy(request):
    return render(request, 'policy.html')


@login_required(login_url='/login')
def add_to_cart(request, id):
    products = Product.objects.get(id=id)
    
    existing_item = Cart.objects.filter(product_id=products.id, user=request.user).first()
    if existing_item:
        if existing_item.quantity >= existing_item.product.stock:
            messages.warning(request, "Product Stock Limited")
        else:
            existing_item.quantity += 1
            existing_item.save()
            messages.success(request, "Product quantity updated in your cart.")
    else:
        if products.stock <= 0:
                messages.warning(request, "Product Stock Limited")
        else:
                Cart.objects.create(product_id=products.id, quantity=1, user=request.user)
                messages.success(request, "Product added to your cart.")

        




    return redirect('home')  # Redirect to the cart page

# views.py
@login_required(login_url='/login')
def view_cart(request):
    cart_products_id = Cart.objects.filter(user=request.user)
    product_id = [x.product_id for x in cart_products_id]
    cart_products = Product.objects.filter(id__in=product_id)
    total_price = sum(x.product_price for x in cart_products)
    context = {
        'cart_products' : cart_products_id,
        'total_price' : total_price
    }
    return render(request,'cart.html',context)
    # return HttpResponse(cart_products[0].produc

def remove_from_cart(request, id):

    # Get the cart item by its ID
    

    cart_item = Cart.objects.get(product_id=id,user=request.user)
    
    # Delete the cart item
    cart_item.delete()
    
    
    # Redirect to the cart page after removal
    return redirect('cart')


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart_item = Cart.objects.get(product_id=product_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('/cart')
    return redirect('/home')

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('home')  # Replace 'home' with your desired redirect
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('/login/')
    

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('home')  # Redirect to home after successful registration
    return render(request, 'register.html')

def checkout(request, id=0):
    if request.method == "POST":
        payment_method = request.POST.get('method')

        if payment_method == 'esewa':
            messages.error(request,'esewa is not available at the moment')
            return HttpResponseRedirect(request.path)
        elif payment_method == 'cod':
            cart_objects = Cart.objects.filter(user=request.user)
            if request.POST.get('address'):
                address = request.POST.get('address')
            else:
                messages.error(request, 'Please provide an address.')
                return HttpResponseRedirect(request.path)
            OrderedBy.objects.create(
                user=request.user,
                address=address,
            )

            for cart_item in cart_objects:
                # Determine size based on the user's selection
                size_option = request.POST.get('size_option')
                size = request.POST.get('custom_size') if size_option == 'custom' else request.POST.get('standard_size')

                # Create an Ordered object
                Ordered.objects.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    size=size,
                    orderedby=OrderedBy.objects.last()
                )

                # Update product stock
                product = Product.objects.filter(id=cart_item.product.id)
                product.update(stock=product[0].stock - cart_item.quantity)

            # Clear the cart after placing the order
            Cart.objects.all().delete()
            return redirect('/')

    # Display checkout page
    if id == 0:
        cart_products = Cart.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.product.product_price for item in cart_products)
        context = {
            'cart_products': cart_products,
            'total_price': total_price
        }
        return render(request, 'checkout.html', context)
    else:
        cart_products = Product.objects.filter(id=id)
        total_price = cart_products[0].product_price
        context = {
            'cart_products': cart_products,
            'total_price': total_price
        }
        return render(request, 'checkout.html', context)

    
@login_required(login_url='/login')
def order_page(request):
    if request.method=="POST":
        id = request.POST.get('id')
        orderby = get_object_or_404(OrderedBy, id=id, user=request.user)
        for x in Ordered.objects.filter(orderedby=orderby):
            product = Product.objects.filter(id=x.product.id)
            product.update(stock = product[0].stock + x.quantity)
        orderby.delete()
        return HttpResponseRedirect(request.path)

       


    ordersby = OrderedBy.objects.filter(user=request.user)
    orders = Ordered.objects.filter(orderedby__in=ordersby)
    context = {
        'ordersby' : ordersby,  
        'orders' : orders
    }
    return render(request,'order_page.html',context)

def add_to_wishlist(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        product.wishlist_users.add(request.user)
        return JsonResponse({'success': True, 'message': 'Product added to wishlist!'})
    return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)
@login_required(login_url='/login')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_products = request.user.wishlist.all()  # Fetch products from the user's wishlist
        return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
    return render(request, 'wishlist.html', {'wishlist_products': []})

@csrf_exempt
def remove_from_wishlist(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        
        # Remove the user from the wishlist_users (ManyToManyField)
        if request.user in product.wishlist_users.all():
            product.wishlist_users.remove(request.user)
            return JsonResponse({'success': True, 'message': 'Product removed from wishlist!'})
        else:
            return JsonResponse({'success': False, 'error': 'Product not in wishlist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

