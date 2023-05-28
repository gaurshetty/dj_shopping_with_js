from django.contrib import admin
from .models import Product, Order, OrderItem, ShipAddress, Brand, Category, WishList, Payment


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'discount', 'stock', 'badge', 'brand', 'category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'placed_date', 'completed_date', 'complete', 'transaction_id']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'order', 'quantity', 'date']


class ShipAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'phone', 'house', 'street', 'city', 'state', 'pincode']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'date']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'transaction_id', 'date', 'pay_method', 'customer_name', 'amount']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShipAddress, ShipAddressAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Payment, PaymentAdmin)

