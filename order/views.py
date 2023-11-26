from django.shortcuts import render
from django.utils import timezone
from .models import PurchaseOrder
# Create your views here.
from rest_framework import viewsets,status
from .serializers import PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class PurchaseOrderViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self,request):
        try:
            query = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message':'no data found'},status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self,request,pk=None):
        try:
            print(pk)
            query = PurchaseOrder.objects.get(pk=pk)
            serializer = PurchaseOrderSerializer(query,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'meassage':'no data found in database'},status=status.HTTP_204_NO_CONTENT)
    
    def create(seld,request,*args,**kwargs):
        data = request.data
        try:
            serializer = PurchaseOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response(e,status=status.HTTP_401_UNAUTHORIZED)
    
    def  update(self,request,pk=None):
        try:
            query = PurchaseOrder.objects.get(pk=pk)
            data = request.data
            serializer = PurchaseOrderSerializer(query,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message':'object not found'})
        
    def destroy(self,request,pk=None):
        try:
            instance = PurchaseOrder.objects.get(pk=pk)
            instance.delete()
            return Response({'message':'object deleted'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message':'object not found'},status=status.HTTP_400_BAD_REQUEST)        

    @action(detail=True,methods=['put','patch'],url_path='acknowledge')
    def acknowledge(self,request,pk=None):
        purchase_order = PurchaseOrder.objects.get(pk=pk)
        purchase_order.acknowledgement_date = request.data['acknowledgement_date']
        purchase_order.save(update_fields=['acknowledgement_date'])

        print('in put call',request.data['acknowledgement_date'])


        return Response({'message':'purhcase order acknowledged'},status=status.HTTP_200_OK)
