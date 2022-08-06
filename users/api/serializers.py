from users import models as users_models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.User
        exclude = ()
        read_only_fields = ["pk","created"]
    