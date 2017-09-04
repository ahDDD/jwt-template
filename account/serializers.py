from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin', 'date_joined', 'last_login', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
