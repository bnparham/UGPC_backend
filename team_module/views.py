from django.shortcuts import render,redirect,reverse
from django.views import View
from account_module.models import User

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
                request.session["send_invite"] = True
        else:
            request.session["user_notFound"] = True
        return redirect(reverse("userPanel"))