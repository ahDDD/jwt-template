from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.response import Response
from account.models import User
from care.constants import DOCTOR_CLASSIFY, DOCTOR_CLASSIFY_DETAIL
from care.models import Post
from care.serializers import DoctorSerializer, PostSerializer


def get_classify(request):
    return JsonResponse(dict(classify=DOCTOR_CLASSIFY), status=200)

def get_classify_detail(request):
    return JsonResponse(dict(classify=DOCTOR_CLASSIFY_DETAIL), status=200)


class DoctorList(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
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
