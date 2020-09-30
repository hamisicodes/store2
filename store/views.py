from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer , complete = False)
        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        

    else:
        items = []
        order = {'get_cart_total':0 , 'get_cart_items':0 , 'shippping':False}
        cart_items = order['get_cart_items']


    products = Product.objects.all()
    context = {'products':products ,'cart_items': cart_items}
    return render(request,'store/store.html' , context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer , complete = False)
        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
       

    else:
        items = []
        order = {'get_cart_total':0 , 'get_cart_items':0 ,'shippping':False}
        cart_items = order['get_cart_items']

    context = {'items':items , 'order':order , 'cart_items': cart_items}
    return render(request,'store/cart.html' , context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer , complete = False)
        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
       

    else:
        items = []
        order = {'get_cart_items':0 , 'get_cart_total':0 ,'shippping':False}
        cart_items = order['get_cart_items']

    context = {'items':items , 'order':order , 'cart_items': cart_items }
    return render(request,'store/checkout.html' , context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ',action)
    print('ProductId: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer = customer , complete = False)
    orderItem,created = OrderItem.objects.get_or_create(order = order , product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer , complete = False)
        total = float(data['form']['total'])
        order.transaction_id  = transaction_id

        b_total = round(order.get_cart_total, 2)

        print(total)
        print(b_total)

        if total == b_total:
            order.complete = True
            print('executed')
        
        order.save()
            
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User not logged in')
        

    return JsonResponse('Payment submitted',safe=False)



