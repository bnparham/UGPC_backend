from django.db.models import Q
from django.shortcuts import render,redirect,reverse
from django.views import View
# Create your views here.
from account_module.models import User
from team_module.models import teamsModel


class userPanelView(View):
    def get(self ,request):

        can_not_send_cap_invite = request.session.get("can_not_send_cap_invite", False)
        send_invite = request.session.get("send_invite", False)
        user_notFound = request.session.get("user_notFound", False)
        if (can_not_send_cap_invite): del (request.session["can_not_send_cap_invite"])
        if (send_invite): del (request.session["send_invite"])
        if (user_notFound) : del (request.session["user_notFound"])

        user = User.objects.get(email__iexact=request.user.email)
        userHasTeam = teamsModel.objects.filter(Q(capitan=user) | Q(teamMate1=user) | Q(teamMate2=user)).exists()
        if(userHasTeam):
            team = teamsModel.objects.get(Q(capitan=user) | Q(teamMate1=user) | Q(teamMate2=user))
            teamName  = team.teamName
        else:
            team = None
            teamName = None
        context = {
            "user": user,
            "userTeam_name": teamName,
            "team": team,
            "can_not_send_cap_invite" : can_not_send_cap_invite,
            "send_invite" : send_invite,
            "user_notFound" : user_notFound,
        }
        if(request.user.is_authenticated):
            return render(request,"userpanel_module/userpanel.html", context)
        return redirect(reverse("home-page"))
