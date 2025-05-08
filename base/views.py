from .models import *
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


@login_required
def store(request):
    products  = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request,'base/store.html',context)

def cart(request):
    cart_items = CartItem.objects.all()
    context = {'cart_items':cart_items}
    return render(request,'base/cart.html',context)

def checkout(request):
    context = {}
    return render(request,'base/checkout.html',context)

@login_required
def profile(request):
    clients = Client.objects.all() 
    context =  {'clients': clients}# Replace with your actual query
    return render(request, 'base/profile.html',context)
    
