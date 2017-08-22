from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
