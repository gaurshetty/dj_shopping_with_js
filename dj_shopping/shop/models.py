import os.path
import uuid
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('product_pics', filename)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    discount = models.IntegerField()
    stock = models.IntegerField()
    colors = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    ratings = models.IntegerField()
    badge = models.CharField(max_length=20)
    image1 = models.ImageField(default='product.jpg', upload_to=get_file_path)
    image2 = models.ImageField(default='product.jpg', upload_to=get_file_path)
    image3 = models.ImageField(default='product.jpg', upload_to=get_file_path)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # ['id', 'name', 'price', 'discount', 'stock', 'colors', 'description', 'ratings', 'badge', 'image', 'date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    placed_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    # ['id', 'user', 'placed_date', 'completed_date', 'complete', 'transaction_id']

    @property
    def shipping(self):
        try:
            address = self.user.address
            return address
        except ObjectDoesNotExist:
            return None

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum(item.get_total for item in items)
        return total

    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        count = sum(item.quantity for item in items)
        return count

    @property
    def is_ship_addr(self):
        if self.shipaddress_set.filter(user=self.user).exists():
            addr = self.shipaddress_set.filter(user=self.user).first()
            return addr
        else:
            return None

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    # ['id', 'product', 'order', 'quantity', 'date']

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShipAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    phone = PhoneNumberField(null=True)
    house = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.IntegerField(null=True)
    # ['id', 'user', 'order', 'phone', 'house', 'street', 'city', 'state', 'pincode']

    def __str__(self):
        return self.city


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    # ['id', 'user', 'product', 'date']

    def __str__(self):
        return self.product.name


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    pay_method = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    card_num = models.CharField(max_length=100, null=True, blank=True)
    expiry = models.CharField(max_length=100, null=True, blank=True)
    cvv = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    account_num = models.CharField(max_length=100, null=True, blank=True)
    ifsc = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    # ['id', 'order', 'transaction_id', 'date', 'pay_method', 'customer_name', 'amount']
