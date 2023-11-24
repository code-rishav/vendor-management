from rest_framework.permissions import BasePermission,IsAuthenticated,IsAuthenticatedOrReadOnly

class VendorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return IsAuthenticated.has_permission(self,request,view)