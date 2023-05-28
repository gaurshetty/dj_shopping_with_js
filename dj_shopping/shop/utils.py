from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.db.models import Q
from xhtml2pdf import pisa
from django.contrib import messages
from .models import Product, Order, OrderItem, ShipAddress, WishList, Payment, Brand, Category


def add_to_cart(request, rd):
    if 'cart' in rd:
        product = Product.objects.get(id=rd['cart'])
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity += 1
        orderItem.save()
        messages.success(request, f'Product {product.name} added to your cart')


def add_wishlist(request, rd):
    if 'add_wishlist' in rd:
        product = Product.objects.get(id=rd['add_wishlist'])
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        messages.success(request, f'Product {product.name} added to your wish list')


def remove_wishlist(request, rd):
    if 'remove_wishlist' in rd:
        product = Product.objects.get(id=rd['remove_wishlist'])
        wishlist = get_object_or_404(WishList, user=request.user, product=product)
        wishlist.delete()
        messages.error(request, f'Product {product.name} removed from your wish list')


def search_product(request, rd):
    if 'search_product' in rd:
        prods = Product.objects.all()
        if rd['price'] != 'nil':
            if rd['price'] == '1':
                prods = prods.filter(price__lt=1000)
            if rd['price'] == '2':
                prods = prods.filter(Q(price__gte=1000) & Q(price__lt=5000))
            if rd['price'] == '3':
                prods = prods.filter(Q(price__gte=5000) & Q(price__lt=10000))
            if rd['price'] == '4':
                prods = prods.filter(Q(price__gte=10000) & Q(price__lt=15000))
            if rd['price'] == '5':
                prods = prods.filter(Q(price__gte=15000) & Q(price__lt=20000))
            if rd['price'] == '6':
                prods = prods.filter(Q(price__gte=20000) & Q(price__lt=30000))
            if rd['price'] == '7':
                prods = prods.filter(Q(price__gte=30000) & Q(price__lt=50000))
            if rd['price'] == '8':
                prods = prods.filter(price__gte=50000)
        if rd['brand'] != 'nil':
            brand = Brand.objects.get(id=rd['brand'])
            prods = prods.filter(brand=brand)
        if rd['category'] != 'nil':
            category = Category.objects.get(id=rd['category'])
            prods = prods.filter(category=category)
        if len(prods) == 0:
            messages.error(request, 'No products found with given criteria!')
            return redirect('new_arrival')
        return prods


def shipping_address(request, data, user, order, shipaddress):
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


def payment_operation(request, payment, data):
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
    return redirect('cart')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_data(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    cart_items = order.get_cart_items
    wishlist = WishList.objects.filter(user=request.user).all()
    prodlist = [list.product.id for list in wishlist]
    return order, cart_items, wishlist, prodlist
# order, cart_items, wishlist, prodlist = get_data(request)

