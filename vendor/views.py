from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.permissions import IsAdminUser

class VendorViewSet(viewsets.ViewSet):
    #set the permission class of the viewset to admin users only
    permission_classes = [IsAdminUser]

    def list(self,request):
        try:
            queryset = Vendor.objects.all()
            serializer = VendorSerializer(queryset,many=True)
        except:
            return Response({'message':'object not found'},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def retrieve(self,request,pk=None):
        try:
            queryset = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(queryset,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Object does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request,*args,**kwargs):
        data = request.data
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self,request,pk=None):
        try:
            queryset = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(queryset,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"object updated"},status=status.HTTP_202_ACCEPTED)
            else:
                print("errors",serializer.errors)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error":"object not found"},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            queryset = Vendor.objects.get(pk=pk)
            queryset.delete()
            return Response({"object deleted"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':'obect not found'},status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='performance')
    def performance(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk) 
            performance_data = {
                'name':vendor.name,
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate,
            }
            return Response(performance_data,status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

