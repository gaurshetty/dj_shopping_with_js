import json
from .models import *
from django.contrib import messages


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': None, 'is_ship_addr': None, 'complete': False}
    cart_items = order['get_cart_items']
    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {'id': product.id, 'name': product.name, 'price': product.price, 'image1': product.image1},
                'quantity': cart[i]['quantity'],
                'get_total': total, }
            items.append(item)
        except:
            pass
    return items, order, cart_items
# items, order, cart_items = cookieCart(request)


def cookieWishlist(request):
    try:
        wishlist = json.loads(request.COOKIES['wishlist'])
    except:
        wishlist = {}
    items = []
    prodlist = []
    for i in wishlist:
        try:
            prodlist.append(int(i))
            product = Product.objects.get(id=i)
            item = product
            items.append(item)
        except:
            pass
    prods = items
    return items, prods, prodlist
# wishlist, prods, prodlist = cookieWishlist(request)


def cartData(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        wishlist = request.user.wishlist_set.all()
        prodlist = [list.product.id for list in wishlist]
        shipaddr = order.is_ship_addr
        order_done = Order.objects.filter(user=request.user, complete=True).all()
    else:
        wishlist, prods, prodlist = cookieWishlist(request)
        order_done = []
        items, order, cart_items = cookieCart(request)
        shipaddr = order['is_ship_addr']
    return items, order, cart_items, wishlist, prodlist, order_done, shipaddr
# items, order, cart_items, wishlist, prodlist, order_done, shipaddr = cartData(request)


def create_shipaddress(request, order, user, data):
    shipaddress, created = ShipAddress.objects.get_or_create(order=order, user=user)
    if order.shipping is not None:
        shipaddress.phone = user.address.phone
        shipaddress.house = user.address.house
        shipaddress.street = user.address.street
        shipaddress.city = user.address.city
        shipaddress.state = user.address.state
        shipaddress.pincode = user.address.pincode
        shipaddress.save()
    else:
        shipaddress.phone = data['phone']
        shipaddress.house = data['house']
        shipaddress.street = data['street']
        shipaddress.city = data['city']
        shipaddress.state = data['state']
        shipaddress.pincode = data['pincode']
        shipaddress.save()

def payment_process(request, order, transaction_id, data):
    payment, created = Payment.objects.get_or_create(order=order, transaction_id=transaction_id)
    if 'card_payment' in data:
        payment.pay_method = 'card_payment'
        payment.customer_name = data['customer_name']
        payment.card_num = data['card_num']
        payment.expiry = data['expiry']
        payment.cvv = data['cvv']
        payment.amount = data['amount']
        payment.save()
        messages.success(request, 'Card payment done successfully!')
    if 'bank_payment' in data:
        payment.pay_method = 'bank_payment'
        payment.customer_name = data['customer_name']
        payment.bank_name = data['bank_name']
        payment.branch = data['branch']
        payment.account_num = data['account_num']
        payment.ifsc = data['ifsc']
        payment.amount = data['amount']
        payment.save()
        messages.success(request, 'Bank payment done successfully!')
    if 'mobile_payment' in data:
        payment.pay_method = 'mobile_payment'
        payment.customer_name = data['customer_name']
        payment.amount = data['amount']
        payment.save()
        messages.success(request, 'Mobile payment done successfully!')
