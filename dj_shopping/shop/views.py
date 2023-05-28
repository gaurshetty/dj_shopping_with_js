import random
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, ShipAddress, WishList, Payment, Brand, Category
from .utils import add_to_cart, add_wishlist, remove_wishlist, search_product, shipping_address, render_to_pdf, \
    payment_operation, get_data
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
invoice_num = 'SN'+str(random.randint(0,999999999999))

# to work this view add form tag with csrf_token for buttons

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rd = request.POST
            add_to_cart(request, rd)
            add_wishlist(request, rd)
            remove_wishlist(request, rd)
        prods = Product.objects.all()
        order, cart_items, wishlist, prodlist = get_data(request)
        context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
        return render(request, 'shop/home.html', context)
    else:
        if request.method == 'POST':
            return redirect('login')
        prods = Product.objects.all()
        context = {'prods': prods}
        return render(request, 'shop/home.html', context)


@login_required()
def product(request):
    if request.method == 'POST':
        rd = request.POST
        add_to_cart(request, rd)
        add_wishlist(request, rd)
        remove_wishlist(request, rd)
    prods = Product.objects.all()
    order, cart_items, wishlist, prodlist = get_data(request)
    context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product.html', context)


@login_required()
def product_detail(request, id):
    if request.method == 'POST':
        rd = request.POST
        add_to_cart(request, rd)
        add_wishlist(request, rd)
        remove_wishlist(request, rd)
    prod = Product.objects.get(id=id)
    order, cart_items, wishlist, prodlist = get_data(request)
    context = {'prod': prod, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product_detail.html', context)


@login_required()
def cart(request):
    if request.method == 'POST':
        rd = request.POST
        if 'clear' in rd:
            order, created = Order.objects.get_or_create(user=request.user, complete=False)
            orderItem = OrderItem.objects.filter(order=order).all()
            orderItem.delete()
        else:
            product = Product.objects.get(id=rd['add_item'])
            order, created = Order.objects.get_or_create(user=request.user, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            if 'Decrease_val' in rd:
                orderItem.quantity -= 1
            if 'Increase_val' in rd:
                orderItem.quantity += 1
            orderItem.save()
            if orderItem.quantity == 0:
                orderItem.delete()
    order, cart_items, wishlist, prodlist = get_data(request)
    orderItem = OrderItem.objects.filter(order=order).all()
    order_done = Order.objects.filter(user=request.user, complete=True).all()
    context = {'items': orderItem, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'order_done': order_done}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = request.POST
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            if order.is_ship_addr is None:
                shipaddress, created = ShipAddress.objects.get_or_create(order=order, user=user)
                shipping_address(request, data, user, order, shipaddress)
            return redirect('payment')
    order, cart_items, wishlist, prodlist = get_data(request)
    orderItem = OrderItem.objects.filter(order=order).all()
    shipaddr = order.is_ship_addr
    context = {'items': orderItem, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'shipaddr': shipaddr}
    return render(request, 'shop/checkout.html', context)


def payment(request):
    transaction_id = invoice_num
    date = datetime.now().strftime("%d/%m/%Y")
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = request.POST
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            if float(data['amount']) == order.get_cart_total + float(45.00):
                order.transaction_id = transaction_id
                order.complete = True
                order.save()
                payment, created = Payment.objects.get_or_create(order=order, transaction_id=transaction_id)
                payment_operation(request, payment, data)
            else:
                messages.error(request, 'Amount payment does not match, try again!')
                return redirect('payment')
    order, cart_items, wishlist, prodlist = get_data(request)
    context = {'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'transaction_id': transaction_id, 'date': date}
    return render(request, 'shop/payment.html', context)

@login_required()
def wishlist(request):
    if request.method == 'POST':
        rd = request.POST
        add_to_cart(request, rd)
        add_wishlist(request, rd)
        remove_wishlist(request, rd)
    order, cart_items, wishlist, prodlist = get_data(request)
    orderItem = OrderItem.objects.filter(order=order).all()
    prods = [list.product for list in wishlist]
    context = {'items': orderItem, 'order': order, 'cart_items': cart_items, 'wishlist': wishlist, 'prods': prods, 'prodlist': prodlist}
    return render(request, 'shop/wishlist.html', context)


@login_required()
def invoice(request, id):
    order = Order.objects.get(id=id)
    orderItem = OrderItem.objects.filter(order=order).all()
    address = ShipAddress.objects.get(order=order)
    order_incomplete, created = Order.objects.get_or_create(user=request.user, complete=False)
    cart_items = order_incomplete.get_cart_items
    wishlist = WishList.objects.filter(user=request.user).all()
    context = {'order': order, 'address': address, 'items': orderItem, 'cart_items': cart_items, 'wishlist': wishlist}
    return render(request, 'shop/invoice.html', context)


@login_required()
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
    return render(request, 'shop/about.html')


@login_required()
def new_arrival(request):
    products = ''
    if request.method == 'POST':
        rd = request.POST
        add_to_cart(request, rd)
        add_wishlist(request, rd)
        remove_wishlist(request, rd)
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
    order, cart_items, wishlist, prodlist = get_data(request)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist, 'brands': brands, 'categories': categories}
    return render(request, 'shop/new_arrival.html', context)


def product_search(request):
    query = request.GET.get("q")
    prods = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    order, cart_items, wishlist, prodlist = get_data(request)
    context = {'prods': prods, 'cart_items': cart_items, 'wishlist': wishlist, 'prodlist': prodlist}
    return render(request, 'shop/product_search.html', context)

