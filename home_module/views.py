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
        notMatch_pass_rePass = request.session.get('notMatch_pass_rePass',False)
        usereditinfo_successfuly = request.session.get('usereditinfo_successfuly',False)
        sendRecoverEmail_msg = request.session.get('sendRecoverEmail_msg',False)
        sendRecoverEmail_NotFound_msg = request.session.get("sendRecoverEmail_NotFound_msg", False)
        reset_pass_success_msg = request.session.get("reset_pass_success_msg", False)
        duplicateUsername_edit = request.session.get("duplicateUsername_edit", False)
        completeAllfields_register_msg = request.session.get("completeAllfields_register_msg", False)
        
        if (email_pass_wrong_msg): del (request.session["email_pass_wrong_msg"])
        if (active_acc_msg): del (request.session["active_acc_msg"])
        if (register_msg) : del (request.session["register_msg"])
        if (duplicate_username) : del (request.session["duplicate_username"])
        if (duplicate_uid) : del (request.session["duplicate_uid"])
        if (duplicate_email) : del (request.session["duplicate_email"])
        if (email_activated) : del (request.session["email_activated"])
        if (email_didnt_activated) : del (request.session["email_didnt_activated"])
        if (failed_register_msg) : del (request.session["failed_register_msg"])
        if(notMatch_pass_rePass) : del (request.session["notMatch_pass_rePass"])
        if(usereditinfo_successfuly) : del (request.session["usereditinfo_successfuly"])
        if(sendRecoverEmail_msg) : del (request.session["sendRecoverEmail_msg"])
        if(sendRecoverEmail_NotFound_msg) : del (request.session["sendRecoverEmail_NotFound_msg"])
        if(reset_pass_success_msg) : del (request.session["reset_pass_success_msg"])
        if(duplicateUsername_edit) : del(request.session["duplicateUsername_edit"])
        if(completeAllfields_register_msg) : del(request.session["completeAllfields_register_msg"])
        

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
            "notMatch_pass_rePass" : notMatch_pass_rePass,
            "usereditinfo_successfuly" : usereditinfo_successfuly,
            "sendRecoverEmail_msg" : sendRecoverEmail_msg,
            "sendRecoverEmail_NotFound_msg" : sendRecoverEmail_NotFound_msg,
            "reset_pass_success_msg" : reset_pass_success_msg,
            "duplicateUsername_edit" : duplicateUsername_edit,
            "completeAllfields_register_msg" : completeAllfields_register_msg,
        }
        return render(request, 'home_module/homePage.html', context)
