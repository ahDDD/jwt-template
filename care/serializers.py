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
        if hasattr(instance, 'profile'):
            return os.path.join('profile', instance.profile.image.name) if instance.profile.image.name else None
        return None

    image = serializers.SerializerMethodField()
    classify = serializers.CharField(source='profile.classify')



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'detail', 'user', 'doctor')


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'doctor', 'update_time', 'id', 'user')
        related_fields = ['doctor', 'user']

    doctor = serializers.CharField(source='doctor.name')
    user = serializers.CharField(source='user.name')


class DoctorSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'team', 'job', 'image', 'classify')
        related_fields = ['doctor', 'comment']

    def get_image(self, instance):
        import os
        # 返回前端服务器地址
        if hasattr(instance, 'profile'):
            return os.path.join('profile', instance.profile.image.name) if instance.profile.image.name else None
        return None

    image = serializers.SerializerMethodField()
    classify = serializers.CharField(source='profile.classify')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', 'user', 'create_time')


class PostUserDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'detail', 'doctor', 'create_time', 'comment', 'id')


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'sex', 'team', 'job', 'age')


class PostDoctorDetailSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'detail', 'user', 'create_time', 'id', 'comment')
