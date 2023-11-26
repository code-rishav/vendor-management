from django.db import models
from django.db.models import F, ExpressionWrapper, DurationField, Sum
from django.utils import timezone
from vendor.models import Vendor
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True,max_length=50)
    vendor = models.ForeignKey(Vendor,on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(null=True)
    delivery_date = models.DateTimeField(null=True)
    actual_delivery_date = models.DateTimeField(null=True,default=None)
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(null=True)
    acknowledgement_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number + "-" + self.vendor.name

@receiver(post_save,sender=PurchaseOrder)  
def update_rating(created, instance,update_fields=None, **kwargs):

    print("*"*20,"presave called")
    object = PurchaseOrder.objects.get(pk=instance.pk)

    if object.status != 'completed' and instance.status == 'completed':
        print("status changed")
        purchase_orders = PurchaseOrder.objects.filter(vendor=instance.vendor)
        total_orders = purchase_orders.count()
        completed_orders = purchase_orders.filter(status='completed')
        order_completed = completed_orders.count()

        #update fulfilment rate
        try:
            fulfilment_rate = completed_orders/total_orders
            instance.vendor.fulfillment_rate = fulfilment_rate
        except ZeroDivisionError:
            print("no orders yet")



        #update ontime delivery rate
        instance.actual_delivery_date = timezone.now()
        current_time = timezone.now()
        ontime_deliveries = purchase_orders.filter(
            actual_delivery_date__lte=current_time,
                delivery_date__lte=current_time,
        ).count()
        print("orders completed",order_completed)
        try:
            rate = ontime_deliveries/order_completed        
            instance.vendor.on_time_delivery_rate = rate
            print("vendor ontime delivery ",instance.vendor.on_time_delivery_rate)
        except ZeroDivisionError:
            print("Zero orders completed")

        #update quality rating average
        # Calculate the average rating
        total_ratings = 0

        # Iterate over all purchase orders for the vendor
        for order in purchase_orders:
            total_ratings += order.quality_rating

        # Calculate the average rating

        # Update the vendor's average rating
        print("total ratings",total_ratings)
        try:
            average_rating = total_ratings / order_completed
            instance.vendor.quality_rating_avg = average_rating
            instance.vendor.name = "newvendor4"
            print("vendor average rating",instance.vendor.quality_rating_avg)
        except ZeroDivisionError:
            print("Zero orders completed")

        #update fulfilment rate
        

        instance.vendor.save()
        print(instance.vendor.vendor_code,"-",instance.vendor.name)
        print("vedndor saved")


    print(update_fields)
    
    if not created and update_fields and 'acknowledgement_date' in update_fields:
        print("acknowledgement changed")
        print(instance.acknowledgement_date)
        purchase_orders = PurchaseOrder.objects.filter(vendor=instance.vendor)

        purchase_orders = purchase_orders.annotate(
            response_time=ExpressionWrapper(
                F('acknowledgement_date') - F('issue_date'),
                output_field=DurationField()
            )
        )

        # Calculate the total response time for all POs of the vendor
        total_response_time = purchase_orders.aggregate(total_time=Sum('response_time'))['total_time']

        # Count the number of POs
        po_count = purchase_orders.count()

        # Calculate the average response time (in seconds)
        average_response_time = total_response_time.total_seconds() / po_count if po_count > 0 else 0

        instance.vendor.average_response_time = average_response_time/3600
        #change the decimal fields properly here in the model itself
        print("average response time",instance.vendor.average_response_time)
        instance.vendor.save()

        #calculate
        #instance.save(update_fields=['acknowledgement_date'])   
        #instance.update()
        """Compute the time difference between issue_date and
        acknowledgment_date for each PO, and then find the average of these times
        for all POs of the vendor."""