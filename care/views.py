from django.http import JsonResponse
from care.constants import DOCTOR_CLASSIFY

def get_classify(request):
    return JsonResponse(dict(classify=DOCTOR_CLASSIFY), status=200)