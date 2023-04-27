from django.urls import path
from .views import inviteEmailView

urlpatterns = [
    path("send-invite/", inviteEmailView.as_view(), name="inviteView")
]