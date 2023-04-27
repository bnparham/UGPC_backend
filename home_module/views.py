from django.shortcuts import render
from django.views import View

# Create your views here.

class HomePageView(View):
    def get(self,request):
        email_pass_wrong_msg = request.session.get("email_pass_wrong_msg", False)
        active_acc_msg = request.session.get("active_acc_msg", False)
        register_msg = request.session.get("register_msg", False)
        if (email_pass_wrong_msg): del (request.session["email_pass_wrong_msg"])
        if (active_acc_msg): del (request.session["active_acc_msg"])
        if (register_msg) : del (request.session["register_msg"])
        context = {
            "email_pass_wrong_msg": email_pass_wrong_msg,
            "active_acc_msg": active_acc_msg,
            "register_msg" : register_msg
        }
        return render(request, 'home_module/homePage.html', context)
