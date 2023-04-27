from django.shortcuts import render,redirect,reverse
from django.views import View
# Create your views here.

class userPanelView(View):
    def get(self,requst):
        context = {}
        if(requst.user.is_authenticated):
            return render(requst,"userpanel_module/userpanel.html", context)
        return redirect(reverse("home-page"))
