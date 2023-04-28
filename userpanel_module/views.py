from django.db.models import Q
from django.shortcuts import render,redirect,reverse
from django.views import View
# Create your views here.
from account_module.models import User
from team_module.models import teamsModel,inviteModel


class userPanelView(View):
    def get(self ,request):
        can_not_send_hasTeam_invite = request.session.get("can_not_send_hasTeam_invite", False)
        send_invite = request.session.get("send_invite", False)
        user_notFound = request.session.get("user_notFound", False)
        group_is_full = request.session.get("group_is_full", False)
        if (can_not_send_hasTeam_invite): del (request.session["can_not_send_hasTeam_invite"])
        if (send_invite): del (request.session["send_invite"])
        if (user_notFound) : del (request.session["user_notFound"])
        if (group_is_full) : del (request.session["group_is_full"])

        user = User.objects.get(email__iexact=request.user.email)
        userHasTeam = teamsModel.objects.filter(Q(capitan=user) | Q(teamMate1=user) | Q(teamMate2=user)).exists()
        if(userHasTeam):
            team = teamsModel.objects.get(Q(capitan=user) | Q(teamMate1=user) | Q(teamMate2=user))
            teamName  = team.teamName
        else:
            team = None
            teamName = None

        invites = inviteModel.objects.filter(reciver=user, is_accept=False, is_reject=False)
        context = {
            "user": user,
            "userTeam_name": teamName,
            "team": team,
            "can_not_send_hasTeam_invite" : can_not_send_hasTeam_invite,
            "send_invite" : send_invite,
            "user_notFound" : user_notFound,
            "invites" : invites,
            "group_is_full": group_is_full,
        }
        if(request.user.is_authenticated):
            return render(request,"userpanel_module/userpanel.html", context)
        return redirect(reverse("home-page"))
