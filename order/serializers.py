from .models import PurchaseOrder
from rest_framework import serializers

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta():
        model = PurchaseOrder
        fields = "__all__"