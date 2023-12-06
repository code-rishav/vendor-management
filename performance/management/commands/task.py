
from vendor.models import Vendor
from ...models import Performance
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "to generate Historical Performance data"
    def handle(self,*args,**options):
        print("*"*15,"task performed")
        vendor_queryset = Vendor.objects.all()

        #create performance record for all vendors
        for vendors in vendor_queryset:
            hist_performance = Performance()
            hist_performance.vendor = vendors
            hist_performance.on_time_delivery_rate = vendors.on_time_delivery_rate
            hist_performance.quality_rating_avg = vendors.quality_rating_avg
            hist_performance.average_response_time = vendors.average_response_time
            hist_performance.fulfillment_rate = vendors.fulfillment_rate
            hist_performance.save()


