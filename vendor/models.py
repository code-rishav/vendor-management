from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100,primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0,blank=True)
    quality_rating_avg = models.FloatField(default=0,blank=True)
    average_response_time = models.FloatField(default=0,blank=True)
    fulfillment_rate = models.FloatField(default=0,blank=True)

    def __str__(self):
        return self.name + self.vendor_code
    