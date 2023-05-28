from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AddressForm
from shop.models import Order, WishList


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'User {} created successfully. Login to access!'.format(username))
            return redirect('login')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'register.html', context={'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', context={'form': form})


@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        a_form = AddressForm(request.POST, instance=request.user.address)
        if u_form.is_valid() and p_form.is_valid() and a_form.is_valid():
            u_form.save()
            p_form.save()
            a_form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the following errors:')
            context = {'u_form': u_form, 'p_form': p_form, 'a_form': a_form}
            return render(request, 'profile.html', context)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        try:
            a_form = AddressForm(instance=request.user.address)
        except ObjectDoesNotExist:
            a_form = AddressForm()
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    cart_items = order.get_cart_items
    wishlist = WishList.objects.filter(user=request.user).all()
    context = {'u_form': u_form, 'p_form': p_form, 'a_form': a_form, 'cart_items': cart_items, 'wishlist': wishlist}
    return render(request, 'profile.html', context)
