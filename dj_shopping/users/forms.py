from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Address
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator


def validate_email(value):
    if value[len(value)-9:] != 'gmail.com':
        raise forms.ValidationError('Email domain should be gmail.com only')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator, validate_email])
    first_name = forms.CharField(max_length=256, validators=[MinLengthValidator(4), MaxLengthValidator(20)])
    last_name = forms.CharField(max_length=256, validators=[MinLengthValidator(4), MaxLengthValidator(20)])
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=256, validators=[MinLengthValidator(4), MaxLengthValidator(20)])
    last_name = forms.CharField(max_length=256, validators=[MinLengthValidator(4), MaxLengthValidator(20)])
    email = forms.EmailField(validators=[EmailValidator, validate_email])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            userdb = User.objects.filter(email=email).first()
            if self.instance != userdb:
                raise ValidationError("Email already exists")
        return email

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         userdb = User.objects.filter(email=email).first()
    #         if self.instance != userdb:
    #             raise ValidationError("Email already exists")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['phone', 'house', 'street', 'city', 'state', 'pincode']
