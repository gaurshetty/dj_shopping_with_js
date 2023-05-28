from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
import os
from phonenumber_field.modelfields import PhoneNumberField


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pics', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpg', upload_to=get_file_path)

    def __str__(self):
        return f'{self.__dict__}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = PhoneNumberField(null=True)
    house = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.IntegerField(null=True)
    # ['phone', 'house', 'street', 'city', 'state', 'pincode']
    class Meta:
        verbose_name_plural = "Addresses"
