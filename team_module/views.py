from django.shortcuts import render,redirect,reverse
from django.views import View
from account_module.models import User
from .models import inviteModel,teamsModel
from django.utils.crypto import get_random_string

# Create your views here.

class inviteEmailView(View):
    def post(self, request):
        email = request.POST.get("InviteEmail")
        user:User = User.objects.filter(email__iexact=email).exists()
        if(user):
            is_cap = User.objects.get(email__iexact=email).is_capitan
            if(is_cap):
                request.session["can_not_send_cap_invite"] = True
            else:
                # invite is send
                request.session["send_invite"] = True
                reciver: User = User.objects.get(email__iexact=email)
                newInvite, created = inviteModel.objects.get_or_create(sender=self.request.user, reciver=reciver, is_accept=False)
                if(created):
                    newInvite.invite_id = get_random_string(25)
                    newInvite.save()
        else:
            request.session["user_notFound"] = True
        return redirect(reverse("userPanel"))

class acceptInvite(View):
    def post(self, request):
        sender = request.POST.get("sender")
        reciver = request.POST.get("reciver")

        sender = User.objects.get(email__iexact=sender)
        reciver = User.objects.get(email__iexact=reciver)

        findTeam = teamsModel.objects.get(capitan=sender)
        if(findTeam.teamMate1 == None):
                reciver.has_team = True
                reciver.save()
                findTeam.teamMate1 = reciver
                findTeam.save()
                findInvite = inviteModel.objects.get(reciver=reciver,sender=sender,is_accept=False)
                findInvite.is_accept=True
                findInvite.save()
        elif(findTeam.teamMate2 == None):
            findTeam.teamMate2 = reciver
            reciver.has_team = True
            reciver.save()
            findTeam.save()
            findInvite = inviteModel.objects.get(reciver=reciver, sender=sender,is_accept=False)
            findInvite.is_accept = True
            findInvite.save()
        else:
            request.session["group_is_full"] = True
        return redirect(reverse("userPanel"))

class removeUserFromTeamView(View):
    def post(self, request):
        teamMateName = request.POST.get("teamMateName")
        teamMateName:User = User.objects.get(email__iexact=teamMateName)
        capitan = request.POST.get("capitan")
        capitan:User = User.objects.get(email__iexact=capitan)
        findTeam = teamsModel.objects.get(capitan=capitan)
        if(findTeam.teamMate1 == teamMateName):
            findTeam.teamMate1 = None
            teamMateName.has_team = False
        else:
            findTeam.teamMate2 = None
            teamMateName.has_team = False
        findTeam.save()
        teamMateName.save()
        return redirect(reverse("userPanel"))

class rejectInvite(View):
    def post(self, request):
        sender = request.POST.get("sender")
        reciver = request.POST.get("reciver")
        sender = User.objects.get(email__iexact=sender)
        reciver = User.objects.get(email__iexact=reciver)
        findInvite = inviteModel.objects.get(sender=sender,reciver=reciver)
        findInvite.is_reject = True
        findInvite.save()
        return redirect(reverse("userPanel"))

