from django.shortcuts import render,redirect,reverse
from django.views import View
from account_module.models import User
from .models import inviteModel,teamsModel

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
                newInvite, created = inviteModel.objects.get_or_create(sender=self.request.user, reciver=reciver)
                if(created):
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
                findTeam.teamMate1 = reciver
                findTeam.save()
                findInvite = inviteModel.objects.get(reciver=reciver,sender=sender)
                findInvite.is_accept=True
                findInvite.save()
        elif(findTeam.teamMate2 == None):
            findTeam.teamMate2 = reciver
            findTeam.save()
            findInvite = inviteModel.objects.get(reciver=reciver, sender=sender)
            findInvite.is_accept = True
            findInvite.save()
        else:
            request.session["group_is_full"] = True
        return redirect(reverse("userPanel"))