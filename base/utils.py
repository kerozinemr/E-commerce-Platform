import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart','{}'))
        print('Cart:', cart)
    except:
            cart = {}
    items = []  
    order ={'get_cart_total':0, 'get_cart_items':0,'shipping':False}  
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
        
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
        
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total,
                }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
                pass
    
    
    return {'cartItems':cartItems ,'order':order, 'items':items}





def cartData(request):
    
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()  # type: ignore
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items'] 
        
    return{'cartItems':cartItems,'order':order, 'items':items}



def guestOrder(request, data):
    print('User Is not logged In..')  
        
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    client, created = Client.objects.get_or_create(
        email=email,
        )
    client.name = name
    client.save()
    
    order = Order.objects.create(
        client=client,
        complete=False,
        )
  
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    return client, order
    