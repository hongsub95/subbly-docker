from rest_framework.permissions import BasePermission

from users.models import User
from markets.models import Market

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        user_id = view.kwargs.get('user_id',None)
        user = User.objects.get(pk=user_id)
        return bool(request.user and user == request.user)

class MarketMasterOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return bool(True)

        market_id = view.kwargs.get('market_id', None)
        market = Market.objects.get(pk=market_id)

        return bool(request.user and market.master == request.user)
        