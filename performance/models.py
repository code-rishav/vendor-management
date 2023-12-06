from django.db import models
from vendor.models import Vendor
from order.models import PurchaseOrder
# Create your models here.
class Performance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor.name +"-"+ str(self.date)

