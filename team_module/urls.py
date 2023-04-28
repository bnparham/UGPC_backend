from django.urls import path
from .views import inviteEmailView,acceptInvite,removeUserFromTeamView,rejectInvite

urlpatterns = [
    path("send-invite/", inviteEmailView.as_view(), name="inviteView"),
    path('accept-invite/', acceptInvite.as_view(), name="accept_invite"),
    path('remove-user/', removeUserFromTeamView.as_view(), name="remove_user"),
    path('reject-user/', rejectInvite.as_view(), name="reject-invite"),
]