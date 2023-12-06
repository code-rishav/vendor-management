from django.db import models
from django.db.models import F, ExpressionWrapper, DurationField, Sum
from django.utils import timezone
from vendor.models import Vendor
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgement_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number + "-" + self.vendor.name

@receiver(post_save,sender=PurchaseOrder)  
def update_rating( instance,update_fields=None, **kwargs):

    #find the related vendors
    object = PurchaseOrder.objects.select_related('vendor')


    #acknowlegement change actions to be performed
    if update_fields and 'acknowledgement_date' in update_fields:
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
        instance.vendor.save()


    #status update changes to be performed
    if instance.status == 'completed':
        purchase_orders = object.filter(vendor=instance.vendor)
        total_orders = purchase_orders.count()
        completed_orders = purchase_orders.filter(status='completed')
        order_completed = completed_orders.count()

        #update fulfilment rate
        if total_orders >0:
            fulfilment_rate = order_completed/total_orders
            instance.vendor.fulfillment_rate = fulfilment_rate
            print("fulfilment rate updated")



        #update ontime delivery rate
        instance.actual_delivery_date = timezone.now()
        current_time = timezone.now()
        ontime_deliveries = purchase_orders.filter(
            actual_delivery_date__lte=current_time,
                delivery_date__lte=current_time,
        ).count()
        try:
            rate = ontime_deliveries/order_completed        
            instance.vendor.on_time_delivery_rate = rate
        except ZeroDivisionError:
            #message to the viewset can be passed through messages
            pass

        #update quality rating average
        # Calculate the average rating
        total_ratings = purchase_orders.values('quality_rating').aggregate(total_rating=Sum('quality_rating'))['total_rating']

        if order_completed>0:
            average_rating = total_ratings / order_completed
            instance.vendor.quality_rating_avg = average_rating
            instance.vendor.name = "newvendor4"

        instance.vendor.save()