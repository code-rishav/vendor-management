from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import VendorPermission

def generate_tokens(vendor):
    refresh = RefreshToken.for_user(vendor)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class VendorViewSet(viewsets.ViewSet):
    permission_classes = [VendorPermission]


    def list(self,request):
        queryset = Vendor.objects.all()
        serializer = VendorSerializer(queryset,many=True)
        print(request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request,*args,**kwargs):
        data = request.data
        print(request)
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print(serializer.error_messages)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self,request,pk=None):
        try:
            queryset = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(queryset,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"Object does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        try:
            queryset = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(queryset,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"object update"},status=status.HTTP_202_ACCEPTED)
            else:
                print("errors",serializer.errors)
                return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error":"object not found"},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            print("delete called")
            print(pk)
            queryset = Vendor.objects.get(pk=pk)
            queryset.delete()
            print("object deleted")
            return Response({"object deleted"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({'error':'obect not found'},status=status.HTTP_404_NOT_FOUND)


