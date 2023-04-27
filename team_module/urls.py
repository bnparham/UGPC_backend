from django.urls import path
from .views import inviteEmailView,acceptInvite

urlpatterns = [
    path("send-invite/", inviteEmailView.as_view(), name="inviteView"),
    path('accept-invite/', acceptInvite.as_view(), name="accept_invite")
]