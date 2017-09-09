from django.http import JsonResponse
from django.http import Http404
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from care.constants import DOCTOR_CLASSIFY, DOCTOR_CLASSIFY_DETAIL
from care.models import Post, Comment
from care.serializers import (
    DoctorSerializer,
    PostSerializer,
    PostListSerializer,
    PostUserDetailSerializer,
    PostDoctorDetailSerializer,
    CommentSerializer
)


def get_classify(request):
    return JsonResponse(dict(classify=DOCTOR_CLASSIFY), status=200)

def get_classify_detail(request):
    return JsonResponse(dict(classify=DOCTOR_CLASSIFY_DETAIL), status=200)


class DoctorList(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        classify = self.kwargs['classify']
        return User.objects.filter(user_type='doctor').filter(profile__classify=classify)


class UserPostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        doctor = User.objects.get(id=self.request.data['doctor'])
        user = User.objects.get(id=self.request.data['user'])
        if doctor.user_type != 'doctor':
            return Response({ 'error': '用户类型有误' }, status=status.HTTP_400_BAD_REQUEST)
        elif request.user != user:
            return Response({'error': '您没有这个权限'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.user_type == 'doctor':
            return Response({'error': '医生不能发起问询'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super(UserPostView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=User.objects.get(id=self.request.data['user']),
            doctor=User.objects.get(id=self.request.data['doctor'])
        )


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.user_type == 'doctor':
            return Post.objects.filter(doctor=self.request.user).order_by('-create_time')
        else:
            return Post.objects.filter(user=self.request.user).order_by('-create_time')


class PostDetailView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_object(self, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        post = self.get_object(id)
        serializer = None
        if request.user.user_type == 'doctor':
            if post.doctor == request.user:
                serializer = PostDoctorDetailSerializer(post)
        else:
            if post.user == request.user:
                serializer = PostUserDetailSerializer(post)
        return Response(serializer.data) if serializer else Response(status=status.HTTP_403_FORBIDDEN)


class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'doctor':
            return Response({'error': '用户类型有误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post = Post.objects.get(id=request.data['post'])
            if post.doctor != request.user:
                return Response({'error': '用户类型有误'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                post.save()
                return super(CommentView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(id=self.request.data['post']))
