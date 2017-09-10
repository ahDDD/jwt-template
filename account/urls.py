from django.conf.urls import url
from account.views import CreateUserView, ChangeUserView, UserViewSet, ProfileImageUpdate, ProfileView, PasswordResetView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    url(r'^register/', CreateUserView.as_view()),   # POST phone=phone&password=password
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),
    url(r'^user/(?P<phone>[0-9]+)/$', ChangeUserView.as_view()),
    url(r'^profile/(?P<user__phone>[0-9]+)/$', ProfileView.as_view()),
    url(r'^profile/(?P<phone>[0-9]+)/image/$', ProfileImageUpdate.as_view()),
    url(r'^user/password_reset/$', PasswordResetView.as_view()),
]

urlpatterns += router.urls
