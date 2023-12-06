from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta():
        model = Vendor
        fields = "__all__"
        read_only_fields = ('on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate')
