from django.conf.urls import url
from account.views import CreateUserView


urlpatterns = [
    url(r'^register/', CreateUserView.as_view()),   # POST email=email&password=password
]