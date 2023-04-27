from django.shortcuts import render,redirect,reverse
from django.views import View
# Create your views here.
from account_module.models import User

class userPanelView(View):
    def get(self,requst):
        user = User.objects.get(email__iexact=requst.user.email)
        context = {
            "user": user
        }
        if(requst.user.is_authenticated):
            return render(requst,"userpanel_module/userpanel.html", context)
        return redirect(reverse("home-page"))
