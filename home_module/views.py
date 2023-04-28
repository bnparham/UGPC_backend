from django.shortcuts import render
from django.views import View

# Create your views here.

class HomePageView(View):
    def get(self,request):
        email_pass_wrong_msg = request.session.get("email_pass_wrong_msg", False)
        active_acc_msg = request.session.get("active_acc_msg", False)
        register_msg = request.session.get("register_msg", False)
        duplicate_username = request.session.get("duplicate_username", False)
        duplicate_uid = request.session.get("duplicate_uid", False)
        duplicate_email = request.session.get("duplicate_email", False)
        email_activated = request.session.get('email_activated',False)
        email_didnt_activated = request.session.get('email_didnt_activated',False)        
        failed_register_msg = request.session.get('failed_register_msg',False)

        
        if (email_pass_wrong_msg): del (request.session["email_pass_wrong_msg"])
        if (active_acc_msg): del (request.session["active_acc_msg"])
        if (register_msg) : del (request.session["register_msg"])
        if (duplicate_username) : del (request.session["duplicate_username"])
        if (duplicate_uid) : del (request.session["duplicate_uid"])
        if (duplicate_email) : del (request.session["duplicate_email"])
        if (email_activated) : del (request.session["email_activated"])
        if (email_didnt_activated) : del (request.session["email_didnt_activated"])
        if (failed_register_msg) : del (request.session["failed_register_msg"])
        

        context = {
            "email_pass_wrong_msg": email_pass_wrong_msg,
            "active_acc_msg": active_acc_msg,
            "register_msg" : register_msg,
            "duplicate_email" : duplicate_email,
            "duplicate_username" : duplicate_username,
            "duplicate_uid" : duplicate_uid,
            "email_activated" : email_activated,
            "email_didnt_activated" : email_didnt_activated,
            "failed_register_msg" : failed_register_msg,
            
        }
        return render(request, 'home_module/homePage.html', context)
