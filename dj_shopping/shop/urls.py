from django.urls import path
# from . import views
from . import views_with_js as views


urlpatterns = [
    path("", views.home, name='home'),
    path("product/", views.product, name='product'),
    path("new_arrival/", views.new_arrival, name='new_arrival'),
    path("product_search/", views.product_search, name='product_search'),
    path("product_detail/<int:id>/", views.product_detail, name='product_detail'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path("update_item/", views.updateItem, name='update_item'),
    path("update_wishlist/", views.updateWishlist, name='update_wishlist'),
    path("payment/", views.payment, name='payment'),
    path("invoice/<int:id>/", views.invoice, name='invoice'),
    path("get_pdf/<int:id>/", views.get_pdf, name='get_pdf'),
    path("wishlist/", views.wishlist, name='wishlist'),
    path("about/", views.about, name='about'),
]

