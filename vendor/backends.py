from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from .models import Vendor
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model


class VendorBackend(BaseBackend):
    def authenticate(self, request, vendor_code=None, password=None):
        print("authentication called ")
        User = get_user_model()
        try:
            print("called authenticate")
            vendor = User.objects.get(vendor_code=vendor_code)
            print(vendor)
            if vendor.password == password:
                return vendor
        except User.DoesNotExist:
            print("error")
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

