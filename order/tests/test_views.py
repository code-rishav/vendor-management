from rest_framework import status
from django.test import TestCase,client
from rest_framework.test import APIRequestFactory,force_authenticate
from django.urls import reverse
from vendor.models import Vendor
from ..models import PurchaseOrder
from ..serializers import PurchaseOrderSerializer
from ..views import PurchaseOrderViewset
from django.contrib.auth.models import User
from django.utils import timezone

factory = APIRequestFactory()
view = PurchaseOrderViewset.as_view({'get':'list','post':'create','put':'update','delete':'destroy'})
user = User.objects.get(username='admin')

class VendorViewTest(TestCase):
    """Test module for all vendor API"""
    def setUp(self):
        vendor = Vendor.objects.create(vendor_code='testvendorcode1',name='test_vendor1', contact_details='contact details',address='address')
        PurchaseOrder.objects.create(po_number='testpo1',vendor=vendor,items={'name':'ABC','price':'123',},quantity=4,status='pending')
        PurchaseOrder.objects.create(po_number='testpo2',vendor=vendor,items={'name':'ABCD','price':'1234',},quantity=5,status='pending')
    
    def test_get_all_po(self):
        #get API response
        request = factory.get('/purchase_orders/')
        force_authenticate(request, user=user)
        response = view(request)
        vendor = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(vendor,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_detail_po(self):
        request = factory.get('/purchase_orders/testpo1/')
        force_authenticate(request,user=user)
        response = view(request)
        vendor = PurchaseOrder.objects.get(pk='testpo1')
        serializer = PurchaseOrderSerializer(vendor,many=False)
        response_data = response.data
        serializer_data = serializer.data
        self.assertEqual(response_data[0],serializer_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_post_detail_po(self):
        po_object = {'po_number':'testpo3','vendor':'testvendorcode1','items':{'name':'ABC','price':'123'},'quantity':4,'status':'pending'}
        request = factory.post('/purchase_orders/',po_object,format='json')
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_put_detail_po(self):
        po = PurchaseOrder.objects.get(pk='testpo2')

        
        updated_data = {
            'po_number':po.po_number,
            'vendor':po.vendor.pk,
            'items':[{'name':'ABC','price':123},{'name':'DEF','price':345}],
            'quantity':6,
            'status':po.status    
    }
        serializer = PurchaseOrderSerializer(instance=po,data=updated_data)
        if serializer.is_valid():
            request = factory.put('/purchase_orders/testpo2/',data=serializer.data,format='json')
            force_authenticate(request,user=user)
            response = view(request,pk='testpo2')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        else:
           self.fail(f"Serializer not valid: {serializer.errors}")

    def test_delete_po(self):
        request = factory.delete('/purchase_orders/testpo2/')
        force_authenticate(request,user=user)
        response = view(request,pk='testpo2')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
