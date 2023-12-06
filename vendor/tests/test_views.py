import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIRequestFactory,force_authenticate
from ..models import Vendor
from ..serializers import VendorSerializer
from ..views import VendorViewSet
from django.contrib.auth.models import User

factory = APIRequestFactory()
view = VendorViewSet.as_view({'get':'list','post':'create','put':'update','delete':'destroy'})
user = User.objects.get(username='admin')

class VendorViewTest(TestCase):
    """Test module for all vendor API"""
    def setUp(self):
        Vendor.objects.create(vendor_code='testvendorcode1',name='test_vendor1', contact_details='contact details1',address='address1')
        Vendor.objects.create(vendor_code='testvendorcode2',name='test_vendor2', contact_details='contact details2',address='address2')
        Vendor.objects.create(vendor_code='testvendorcode3',name='test_vendor3', contact_details='contact details3',address='address3')
    
    def test_get_all_vendor(self):
        request = factory.get('/vendor/')
        force_authenticate(request, user=user)
        response = view(request)
        vendor = Vendor.objects.all()
        serializer = VendorSerializer(vendor,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_detail_vendor(self):
        request = factory.get('vendor/testvendorcode1/')
        force_authenticate(request,user=user)
        response = view(request)
        vendor = Vendor.objects.get(pk='testvendorcode1')
        serializer = VendorSerializer(vendor,many=False)
        response_data = response.data
        serializer_data = serializer.data
        self.assertEqual(response_data[0],serializer_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_post_detail_vendor(self):
        vendor_object = {'vendor_code':'dummyvendorcode1','name':'dummy_vendor1', 'contact_details':'contact details1','address':'address1'}
        request = factory.post('/vendor/',vendor_object)
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_put_detail_vendor(self):
        vendor = Vendor.objects.get(pk='testvendorcode2')

        updated_name = 'changednamevendor2'
        updated_data = {
        'vendor_code': vendor.vendor_code,
        'name': updated_name,
        'contact_details': vendor.contact_details,
        'address': vendor.address,
    }
        serializer = VendorSerializer(instance=vendor,data=updated_data)
        if serializer.is_valid():
            request = factory.put('/vendor/testvendorcode2/',data=serializer.data)
            force_authenticate(request,user=user)
            response = view(request,pk='testvendorcode2')
        
            self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        else:
           self.fail(f"Serializer not valid: {serializer.errors}")

    def test_delete_vendor(self):
        request = factory.delete('/vendor/testvendorcode3/')
        force_authenticate(request,user=user)
        response = view(request,pk='testvendorcode3')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_performance_vendor(self):
        request = factory.get('/vendor/testvendorcode3/performance')
        force_authenticate(request,user)
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_200_OK)