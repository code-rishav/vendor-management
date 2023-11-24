from django.db import models
from vendor.models import Vendor

# Create your models here.
class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True,max_length=50)
    vendor = models.ForeignKey(Vendor,on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.po_number + " " + self.vendor.name



