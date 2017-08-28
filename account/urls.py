from django.conf.urls import url
from account.views import CreateUserView, ChangeUserView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


urlpatterns = [
    url(r'^register/', CreateUserView.as_view()),   # POST phone=phone&password=password
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),
    url(r'^user/(?P<phone>[0-9]+)/$', ChangeUserView.as_view()),
]
