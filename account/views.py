from rest_framework import permissions
from rest_framework import mixins, generics
from account.serializers import User, UserSerializer


class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
