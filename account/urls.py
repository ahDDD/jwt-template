from django.conf.urls import url
from account.views import CreateUserView, ChangeUserView, UserViewSet, ProfileUpdate
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
# router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    url(r'^register/', CreateUserView.as_view()),   # POST phone=phone&password=password
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh/', refresh_jwt_token),
    url(r'^user/(?P<phone>[0-9]+)/$', ChangeUserView.as_view()),
    url(r'^profile/(?P<phone>[0-9]+)/$', ProfileUpdate.as_view()),
]

urlpatterns += router.urls
