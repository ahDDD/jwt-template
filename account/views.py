import os
from datetime import datetime, timedelta
from django.http import Http404
from rest_framework import permissions
from rest_framework import mixins, generics
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler
from django.core.mail import send_mail
from django.conf import settings
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


class ProfileImageUpdate(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly)

    def get_object(self, phone):
        try:
            return DoctorProfile.objects.get(user__phone=phone)
        except DoctorProfile.DoesNotExist:
            raise Http404

    def post(self, request, phone, format=None):
        try:
            if request.data['files']:
                profile = self.get_object(phone)
                profile.image.delete()
                profile.image = request.data['files']
                upload = request.data['files']
                profile.image.save(upload.name, upload)
                file = os.path.join('profile', profile.image.name)
                return Response(dict(file=file))
            else:
                return Response(dict(errcode=400), status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(dict(errcode=400), status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = DoctorProfile.objects.all().select_related('user')
    permission_classes = (permissions.IsAuthenticated, IsProfileOwnerOrReadOnly)
    serializer_class = ProfileSerializer
    lookup_field = 'user__phone'


class PasswordForgotView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            user = User.objects.get(phone=request.data['user'])
        except User.DoesNotExist:
            raise Http404
        exp = int((datetime.now() + timedelta(hours=1)).timestamp()) * 1000
        token = jwt_encode_handler(dict(user=user.phone, exp=exp))
        title = '[Cool]密码重置申请'
        content = '''{}, 您好,
        您最近申请了重设密码, 请点击下面的链接设置新密码:
        {}/setting/reset?token={}
        
        请勿回复此邮件
        '''.format(user.name, settings.HOST, token.replace('.', '_'))
        send_mail(
            title,
            content,
            'cool',
            [user.email],
            fail_silently=False
        )
        return Response({'status': 'done'})


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            token = request.data['token']
            payload = jwt_decode_handler(token)
        except:
            return Response(dict(error='token错误'), status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone=request.data['user'])
        except User.DoesNotExist:
            raise Http404
        if payload.get('user') != user.phone:
            return Response(dict(error='token错误'), status=status.HTTP_400_BAD_REQUEST)
        exp = int(datetime.now().timestamp()) * 1000
        if payload.get('exp', 0) > exp:
            user.set_password(request.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(dict(error='token过期'), status=status.HTTP_400_BAD_REQUEST)
