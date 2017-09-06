from rest_framework import serializers
from account.models import User, DoctorProfile


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin', 'date_joined', 'last_login', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin', 'date_joined', 'last_login', 'id', 'password')
        related_fields = ['profile']

    image = serializers.FileField(source='profile.image')
    classify = serializers.CharField(source='profile.classify')


class UserChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('image', 'classify')
        related_fields = ['user']
