from django.test import TestCase
from ..models import Vendor

class VendorTest(TestCase):
    """Test module for vendor model"""
    def setUp(self):
        Vendor.objects.create(vendor_code='testvendorcode1',name='test_vendor1', contact_details='contact details',address='address')

    def test_vendor(self):
        vendor_test1 = Vendor.objects.get(pk='testvendorcode1')
        self.assertEqual(vendor_test1.name,"test_vendor1")


