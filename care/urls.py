from django.conf.urls import url
from care.views import get_classify, get_classify_detail, DoctorList, UserPostView

urlpatterns = [
    url(r'^get_classify/', get_classify),
    url(r'^get_classify_detail/', get_classify_detail),
    url(r'^doctor/(?P<classify>[A-Z]+)/$', DoctorList.as_view()),
    url(r'^post/$', UserPostView.as_view()),
]