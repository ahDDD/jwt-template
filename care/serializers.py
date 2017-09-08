from rest_framework import serializers
from account.models import User
from care.models import Post, Comment

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'sex', 'team', 'job', 'email', 'image', 'classify', 'id')
        related_fields = ['profile']

    def get_image(self, instance):
        import os
        # 返回前端服务器地址
        return os.path.join('profile', instance.profile.image.name) if instance.profile else ''

    image = serializers.SerializerMethodField()
    classify = serializers.CharField(source='profile.classify')



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'detail', 'user', 'doctor')
