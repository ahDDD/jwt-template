from rest_framework import serializers
from account.models import User, DoctorProfile


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin', 'date_joined', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin', 'date_joined', 'last_login', 'password')
        related_fields = ['profile']

    def get_image(self, instance):
        import os
        # 返回前端服务器地址
        return os.path.join('profile', instance.profile.image.name) if hasattr(instance, 'profile') else ''

    image = serializers.SerializerMethodField()
    classify = serializers.CharField(source='profile.classify')


class UserChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('classify', )
        lookup_field = 'user__phone'
