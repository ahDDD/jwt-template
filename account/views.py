from rest_framework import permissions
from rest_framework import mixins, generics
from account.serializers import User, UserSerializer, UserCreateSerializer, UserChangePasswordSerializer
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status


class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ChangeUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'phone'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
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