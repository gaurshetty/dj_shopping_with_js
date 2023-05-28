from django.contrib import admin
from .models import Profile, Address
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image']


class AddressForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='IN'),
        }


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ['id', 'user', 'phone', 'house', 'street', 'city', 'state', 'pincode']


admin.site.register(Profile, ProfileAdmin)

