import os
from django.http import Http404
from rest_framework import permissions
from rest_framework import mixins, generics
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from account.serializers import (
    User,
    UserSerializer,
    UserCreateSerializer,
    UserChangePasswordSerializer,
    DoctorProfile,
    ProfileSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import detail_route, parser_classes
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsOwnerOrReadOnly, IsProfileOwnerOrReadOnly


class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ChangeUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserSerializer
    lookup_field = 'phone'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'phone'

    @detail_route(methods=['post'])
    def set_password(self, request, phone=None):
        user = self.get_object()
        password = request.data.get('password')
        new_password = request.data.get('newPassword')
        if user.check_password(password):
            user.set_password(new_password)
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response({'status': '密码验证错误'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfile
    permission_classes = (permissions.IsAuthenticated, IsProfileOwnerOrReadOnly)
    lookup_field = 'user__phone'

    def pre_save(self, obj):
        obj.image = self.request.FILES.get('file')


class ProfileUpdate(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly)

    def get_object(self, phone):
        try:
            return DoctorProfile.objects.get(user__phone=phone)
        except DoctorProfile.DoesNotExist:
            raise Http404

    def post(self, request, phone, format=None):
        try:
            profile = self.get_object(phone)
            profile.image.delete()
            profile.image = request.data['files']
            upload = request.data['files']
            profile.image.save(upload.name, upload)
            file = os.path.join('profile', profile.image.name)
            return Response(dict(file=file), status=204)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
