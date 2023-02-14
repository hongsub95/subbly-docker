from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        
        
