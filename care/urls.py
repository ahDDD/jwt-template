from django.conf.urls import url
from care.views import get_classify

urlpatterns = [
    url(r'^get_classify/', get_classify)
]