from rest_framework import routers
from django.urls import path,include
from .views import PurchaseOrderViewset

routers = routers.DefaultRouter()

routers.register(r'purchase_orders',PurchaseOrderViewset,basename='pruchase-order')

urlpatterns = [
    path('',include(routers.urls))
]