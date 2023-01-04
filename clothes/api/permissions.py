from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, clothes):
        if clothes.host == request.user :
            return bool(True)
