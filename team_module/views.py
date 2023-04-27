from django.shortcuts import render,redirect,reverse
from django.views import View
from account_module.models import User
from .models import inviteModel

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