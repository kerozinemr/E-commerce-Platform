import json
import datetime
from os import remove
from django.http import JsonResponse
from .models import *
from .utils import *
from django.shortcuts import render, redirect
from . import forms
from .decorators import *
from .forms import ClientForm , CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import authenticate, login, logout



@unauthenticated_user
def register(request):
    
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('login')
        else:
            messages.error(request,'U have an error but the developer is too smart to tell u what is it, good luck ;)')
    context = {'form':form}
    return render(request, 'base/register.html',context)
    
@unauthenticated_user    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Welcome!',user.username)
            return redirect('store')
        
        
        else:
            messages.info(request,'Username OR Password is Incorrect!')
    context = {'messages':messages}
    return render(request,'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login') 



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
  
    products  = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, 'cartItems':cartItems}
    return render(request,'base/store.html',context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items ,'order':order, 'cartItems':cartItems}
    return render(request,'base/cart.html',context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']  
        
    context = {'items':items ,'order':order, 'cartItems':cartItems}
    return render(request,'base/checkout.html',context)

@login_required
def profile(request):
    client = request.user.client
    user = request.user
    form = ClientForm(instance=client)
    clients = Client.objects.get(user=user) 

    if request.method == 'POST':
        print("POST request received")
        print("FILES:", request.FILES)
        
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            print("Form is valid")
            try:
                form.save()
                print("Form saved successfully")
                
            except Exception as e:
                print(f"Error saving form: {e}")
                
        else:
            print("Form errors:", form.errors)

    context =  {'clients': clients, 'form':form}
    return render(request, 'base/profile.html',context)
    
    
    
    
    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action: ',action)
    print('productId: ', productId)
    if request.user.is_authenticated:
        client = request.user.client
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(client=client, complete=False)
        
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    else:
        
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(client=blank ,complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) 
        print('add button clicked')
    elif action =='remove':
         orderItem.quantity = (orderItem.quantity - 1) # type: ignore
    
    orderItem.save()
    cart_items = order.get_cart_items
    
    if orderItem.quantity <= 0: # type: ignore
           orderItem.delete()
    print(client)
    return JsonResponse({
    'message': 'Item was added',
    'cartItems': cart_items
    }, safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
          
           
    else:
        client, order = guestOrder(request, data)
        
        
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()  

    if order.shipping == True:
        
        ShippingAddress.objects.create(
            client=client,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
            
    return JsonResponse({'message':'Payment completed...'}, safe=False )

