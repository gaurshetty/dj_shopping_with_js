import json
import random
import time
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, ShipAddress, WishList, Payment, Brand, Category
from .utils import add_to_cart, add_wishlist, remove_wishlist, search_product, shipping_address, render_to_pdf, \
    payment_operation, get_data
from .utils_with_js import cookieCart, cookieWishlist, cartData, payment_process, create_shipaddress
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
invoice_num = 'SN'+str(random.randint(0, 999999999999))


def home(request):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    prods = Product.objects.all()
    context = {'prods': prods, 'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/home.html', context)


def product(request):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    prods = Product.objects.all()
    context = {'prods': prods, 'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product.html', context)


def product_detail(request, id):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    prod = Product.objects.get(id=id)
    context = {'prod': prod, 'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product_detail.html', context)


def cart(request):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist, 'order_done': order_done}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        wishlist = request.user.wishlist_set.all()
        prodlist = [list.product.id for list in wishlist]
        shipaddr = order.is_ship_addr
        if request.method == 'POST':
            data = request.POST
            if order.is_ship_addr is None:
                create_shipaddress(request, order, user, data)
            return redirect('payment')
    else:
        wishlist, prods, prodlist = cookieWishlist(request)
        items, order, cart_items = cookieCart(request)
        shipaddr = order['is_ship_addr']
        if request.method == 'POST':
            data = request.POST
            try:
                user = User.objects.get(email=data['email'])
                if user:
                    messages.error(request, 'Email already exists, try with another email!')
                    return redirect('checkout')
            except ObjectDoesNotExist:
                request.session['user'] = data
                return redirect('payment')

    context = {'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist, 'shipaddr': shipaddr}
    return render(request, 'shop/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    action = data['action']
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    if action == 'clear':
        orderItems = OrderItem.objects.filter(order=order).all()
        orderItems.delete()
        return redirect('cart')
    productId = data['productId']
    product = Product.objects.get(id=productId)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def updateWishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = request.user
    product = Product.objects.get(id=productId)
    if action == 'add':
        wishlist, created = WishList.objects.get_or_create(user=user, product=product)
    elif action == 'remove':
        wishlist = get_object_or_404(WishList, user=request.user, product=product)
        wishlist.delete()
    return JsonResponse('Action on wishlist', safe=False)


def payment(request):
    transaction_id = invoice_num
    date = datetime.now().strftime("%d/%m/%Y")
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        wishlist = request.user.wishlist_set.all()
        prodlist = [list.product.id for list in wishlist]
        if request.method == 'POST':
            data = request.POST
            if float(data['amount']) == order.get_cart_total + float(45.00):
                order.transaction_id = transaction_id
                order.complete = True
                order.save()
                payment_process(request, order, transaction_id, data)
                return redirect('cart')
            else:
                messages.error(request, 'Amount payment does not match, try again!')
                return redirect('payment')
    else:
        wishlist, prods, prodlist = cookieWishlist(request)
        items, order, cart_items = cookieCart(request)
        userdata = request.session['user']
        if request.method == 'POST':
            data = request.POST
            if float(data['amount']) == order['get_cart_total'] + float(45.00):
                order['complete'] = True
                user = User.objects.create(username=userdata['email'], first_name=userdata['first_name'], last_name=userdata['last_name'], email=userdata['email'],)
                order_db, created = Order.objects.get_or_create(user=user, complete=False)
                for item in items:
                    prod = Product.objects.get(id=item['product']['id'])
                    OrderItem.objects.create(order=order_db, product=prod, quantity=item['quantity'])
                create_shipaddress(request, order_db, user, userdata)
                order_db.transaction_id = transaction_id
                order_db.complete = True
                order_db.save()
                payment_process(request, order_db, transaction_id, data)
                try:
                    del request.session['user']
                except KeyError:
                    print('Session not cleared')
                # return redirect('cart')
                response = redirect('cart')
                response.delete_cookie('cart')
                return response
            else:
                messages.error(request, 'Amount payment does not match, try again!')
                return redirect('payment')
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist,
               'transaction_id': transaction_id, 'date': date}
    return render(request, 'shop/payment.html', context)


def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        wishlist = request.user.wishlist_set.all()
        prods = [list.product for list in wishlist]
        prodlist = [list.product.id for list in wishlist]
    else:
        items, order, cart_items = cookieCart(request)
        wishlist, prods, prodlist = cookieWishlist(request)
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prods': prods, 'prodlist': prodlist}
    return render(request, 'shop/wishlist.html', context)


def invoice(request, id):
    order = Order.objects.get(id=id)
    orderItem = OrderItem.objects.filter(order=order).all()
    address = ShipAddress.objects.get(order=order)
    order_incomplete, created = Order.objects.get_or_create(user=request.user, complete=False)
    cart_items = order_incomplete.get_cart_items
    wishlist = WishList.objects.filter(user=request.user).all()
    context = {'order': order, 'address': address, 'items': orderItem, 'cart_items': cart_items, 'wishlist': wishlist}
    return render(request, 'shop/invoice.html', context)


def get_pdf(request, id):
    firstname = request.user.first_name
    lastname = request.user.last_name
    user = f'{firstname} {lastname}'
    order = Order.objects.get(id=id)
    orderItem = OrderItem.objects.filter(order=order).all()
    address = ShipAddress.objects.get(order=order)
    context = {'user': user, 'order': order, 'address': address, 'items': orderItem}
    pdf = render_to_pdf('shop/pdf_get.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, 'shop/pdf.html', context)


def about(request):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/about.html', context)


def new_arrival(request):
    products = ''
    if request.method == 'POST':
        rd = request.POST
        products = search_product(request, rd)
    if products == '':
        prods = Product.objects.all()
        paginator = Paginator(prods, 3)
        page_number = request.GET.get('page')
        try:
            prods = paginator.page(page_number)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)
    else:
        prods = products
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist, 'brands': brands, 'categories': categories}
    return render(request, 'shop/new_arrival.html', context)


def product_search(request):
    items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)
    query = request.GET.get("q")
    prods = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product_search.html', context)

