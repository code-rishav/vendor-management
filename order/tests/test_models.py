from django.test import TestCase
from ..models import PurchaseOrder
from vendor.models import Vendor

class VendorTest(TestCase):
    """Test module for vendor model"""
    def setUp(self):
        vendor = Vendor.objects.create(vendor_code='testvendorcode1',name='test_vendor1',password='password1', contact_details='contact details',address='address')
        PurchaseOrder.objects.create(po_number='testpo1',vendor=vendor,items={'name':'ABC','price':'123',},quantity=4,status='pending')
        PurchaseOrder.objects.create(po_number='testpo2',vendor=vendor,items={'name':'ABCd','price':'1234',},quantity=5,status='pending')


    def test_vendor(self):
        po_test1 = PurchaseOrder.objects.get(pk='testpo1')
        self.assertEqual(po_test1.vendor.pk,"testvendorcode1")


