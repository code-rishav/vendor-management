from django.urls import path,include
from rest_framework import routers

from .views import VendorViewSet
routers = routers.DefaultRouter()
routers.register(r'vendor',VendorViewSet,basename='vendors')

urlpatterns = [
    path('',include(routers.urls))
]