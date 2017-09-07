from django.http import JsonResponse
from account.models import User
from care.constants import DOCTOR_CLASSIFY, DOCTOR_CLASSIFY_DETAIL
from care.serializers import DoctorSerializer
from rest_framework import status, generics
from rest_framework import permissions

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
