from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login,logout
from django.db.models import Q

from account_module.forms import Register_Form, Login_Form, EditUserInfoForm, ForgotPasswordForm, ResetPasswordForm
from team_module.models import teamsModel

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

class RegisterView(View):
    def get(self, request):
        register_form = Register_Form(request=request)
        context = {
            "register_form": register_form
        }
        if(request.user.is_authenticated):
            return redirect(reverse("home-page"))
        return render(request, "account_module/register_page.html", context)

    def post(self, request):
        register_form = Register_Form(request.POST, request=request)
        if(register_form.is_valid()):
            user_email = register_form.cleaned_data.get("email")
            user_uid = register_form.cleaned_data.get("uid")
            user_username = register_form.cleaned_data.get("username")
            user_name = register_form.cleaned_data.get("name")
            user : bool = User.objects.filter(email__iexact=user_email).exists()
            if(User.objects.filter(username=user_username).exists()):
                request.session["duplicate_username"] = True
                return redirect(reverse("home-page"))
            if(User.objects.filter(uid=user_uid).exists()):
                request.session["duplicate_uid"] = True
                return redirect(reverse("home-page"))
            if(user):
                # register_form.add_error("email", "ایمیل وارد شده متعلق به حساب کاربری دیگری میباشد")
                request.session["duplicate_email"] = True
                return redirect(reverse("home-page"))
            else:
                user_pass = register_form.cleaned_data.get("password")
                if(user_email!="" or user_username!="" or user_name!="" or user_pass!="" or user_uid != ""):
                    if(len(user_pass) <= 8):
                        request.session["password_len_error_register_msg"] = True
                        return redirect(reverse("home-page"))
                    if(len(user_uid) != 13):
                        request.session["uid_len_error_register_msg"] = True
                        return redirect(reverse("home-page"))
                    new_user = User(
                        email=user_email,
                        is_active=False,
                        email_activation_code=0,
                        uid=user_uid,
                        first_name=user_name,
                        username=user_username,
                    )
                    new_user.set_password(user_pass)
                    new_user.save()
                    new_user.email_activation_code = account_activation_token.make_token(new_user)
                    new_user.save()

                    #email
                    to_email=user_email
                    mail_subject = 'حساب کاربری رو فعال کن!'
                    message = render_to_string('account_module/email_activation.html', {
                        'user': user_username,
                        'full_name': f'{user_name}',
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': account_activation_token.make_token(new_user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    })
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    if email.send():
                        request.session["register_msg"] = True
                    else:
                        request.session["failed_register_msg"] = True
                        new_user.delete()
                    return redirect(reverse("home-page"))
                else:
                    request.session["completeAllfields_register_msg"] = True
                    return redirect(reverse("home-page"))
        return redirect(reverse("home-page"))
    
    def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            request.session['email_activated']=True
            login(request,user)
            return redirect(reverse("home-page"))
        else:
            request.session['email_didnt_activated']=True
            
        return redirect(reverse("home-page"))
    

class LoginVeiw(View):
    def get(self, request):
        login_form = Login_Form()
        register_msg = request.session.get("register_msg", False)
        logout_msg = request.session.get("logout_msg", False)
        if(register_msg): del(request.session["register_msg"])
        if(logout_msg): del(request.session["logout_msg"])
        context = {
            "login_form": login_form,
            "register_msg": register_msg,
            "logout_msg": logout_msg
        }
        if(request.user.is_authenticated):
            return redirect(reverse("home-page"))
        return render(request, "account_module/login_page.html", context)

    def post(self, request):
        login_form = Login_Form(request.POST)
        if(login_form.is_valid()):
            user_email = login_form.cleaned_data.get("email")
            user_password = login_form.cleaned_data.get("password")
            user : User = User.objects.filter(email__iexact=user_email).first()
            if(user is not None):
                if(user.is_active):
                    check_pass = user.check_password(user_password)
                    if (check_pass):
                        login(request, user)
                        return redirect(reverse("home-page"))
                    else:
                        # login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
                        request.session["email_pass_wrong_msg"] = True
                else:
                    # login_form.add_error("password", "حساب کاربری شما فعال نمیباشد")
                    request.session["active_acc_msg"] = True
            else:
                # login_form.add_error("password", "ایمیل یا رمز عبور نادرست میباشد")
                request.session["email_pass_wrong_msg"] = True
        return redirect(reverse("home-page"))

class logoutView(View):
    def get(self, request):
        logout(request)
        request.session["logout_msg"] = True
        request.session.set_expiry(1)
        return redirect(reverse("home-page"))

class changeUserType(View):
    def get(self, request):
        empty_teamName_msg = request.session.get("empty_teamName_msg", False)
        if(empty_teamName_msg): del(request.session["empty_teamName_msg"])

        user:User = User.objects.get(email__iexact=request.user.email)
        findUserTeam = teamsModel.objects.filter(capitan=user).exists()
        if(findUserTeam):
            userTeamName = teamsModel.objects.get(capitan=user).teamName
        else:
            userTeamName = False
        context = {
            "userTeamName" : userTeamName,
            "empty_teamName_msg" : empty_teamName_msg,
        }
        return render(request, "account_module/userType.html", context)

    def post(self, request):
        is_cap = int(request.POST.get("options-outlined"))
        user:User = User.objects.get(email__iexact=request.user.email)
        findUserTeam = teamsModel.objects.filter(capitan=user).exists()
        if is_cap == 1 and not user.is_capitan:
            user.is_capitan = True
            findGroupThatHasThisUser = teamsModel.objects.filter(Q(teamMate1=user) | Q(teamMate2=user)).exists()
            if(findGroupThatHasThisUser):
                try:
                    t = teamsModel.objects.get(teamMate1=user)
                    t.teamMate1 = None
                except:
                    t = teamsModel.objects.get(teamMate2=user)
                    t.teamMate2 = None
                t.save()
            user.save()
        elif is_cap == 0 and user.is_capitan:
            user.is_capitan = False
            user.has_team = False
            if findUserTeam:
                if(teamsModel.objects.get(capitan=user).teamMate1 is not None):
                    teammate1 = teamsModel.objects.get(capitan=user).teamMate1
                    teammate1.has_team = False
                    teammate1.save()
                elif(teamsModel.objects.get(capitan=user).teamMate2 is not None):
                    teammate2 = teamsModel.objects.get(capitan=user).teamMate2
                    teammate2.has_team = False
                    teammate2.save()
                teamsModel.objects.filter(capitan=user).delete()
            user.save()
        elif is_cap == 1 and user.is_capitan:
            group_name:str = request.POST.get("teamName")
            if findUserTeam:
                teamName = teamsModel.objects.get(capitan=user)
                if teamName.teamName != group_name and group_name != "" and len(group_name.strip())!=0:
                    teamName.teamName = group_name.strip()
                    teamName.save()
            else:
                if(group_name == None or group_name == "" or len(group_name)==0):
                    request.session["empty_teamName_msg"] = True
                else:
                    newTeam = teamsModel(capitan=user, teamName=group_name, teamMate1=None, teamMate2=None)
                    user.has_team = True
                    newTeam.save()
                    user.save()
        return redirect(reverse("userPanel"))

class editUserInfo(View):
    def get(self, request):
        user = self.request.user
        user = User.objects.get(email__iexact=user)
        initial = {"username":user.username,"name":user.first_name,"uid":user.uid}
        edituserinfo_form = EditUserInfoForm(initial=initial)
        context = {
            "edit_form" : edituserinfo_form
        }
        return render(request, "account_module/editUserInfo.html", context)

    def post(self, request):
        edituserinfo_form = EditUserInfoForm(request.POST)
        user = self.request.user
        user = User.objects.get(email__iexact=user)
        if(edituserinfo_form.is_valid()):
            get_username = edituserinfo_form.cleaned_data.get("username")
            if(user.username != get_username):
                if(User.objects.filter(username__iexact=get_username).exists()):
                    request.session["duplicateUsername_edit"] = True
                    return redirect((reverse("home-page")))
                else:
                    user.username = get_username
            get_name = edituserinfo_form.cleaned_data.get("name")
            get_uid = edituserinfo_form.cleaned_data.get("uid")
            user.first_name = get_name
            user.uid = get_uid
            user.save()
            request.session["usereditinfo_successfuly"] = True
        return redirect(reverse("home-page"))

class ForgetPassword(View):
    def get(self, request):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                # send reset password email to user
                #todo:send email
                #email
                to_email=user_email
                mail_subject = 'فراموشی رمز عبور'
                message = render_to_string('account_module/recover_pass_email.html', {
                    'user': user,
                    'full_name': f'{user.first_name}',
                    "email_activation_code" : user.email_activation_code,
                    'domain': get_current_site(request).domain,
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'

                if email.send():
                    request.session["sendRecoverEmail_msg"] = True
                else:
                    request.session["sendRecoverEmail_NotFound_msg"] = True

            else:
                request.session["sendRecoverEmail_NotFound_msg"] = True

        return redirect(reverse("home-page"))


class ResetPassword(View):
    def get(self, request, active_code):

        reset_pass_notMatch_confirmPass = request.session.get("reset_pass_notMatch_confirmPass", False)
        password_len_error_reset_msg = request.session.get("password_len_error_reset_msg", False)

        if (reset_pass_notMatch_confirmPass): del (request.session["reset_pass_notMatch_confirmPass"])
        if (password_len_error_reset_msg) : del (request.session["password_len_error_reset_msg"])

        user = User.objects.filter(email_activation_code=active_code).first()
        if user is None:
            return redirect(reverse('home-page'))
        reset_pass_form = ResetPasswordForm()
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user,
            "reset_pass_notMatch_confirmPass" : reset_pass_notMatch_confirmPass,
            "password_len_error_reset_msg" : password_len_error_reset_msg,
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_activation_code=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('home-page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            if (len(user_new_pass) <= 8):
                request.session["password_len_error_reset_msg"] = True
                return redirect(reverse("reset_password_page" ,kwargs={"active_code":user.email_activation_code}))
            user_new_confirmPass = reset_pass_form.cleaned_data.get("confirm_password")
            if(user_new_pass == user_new_confirmPass):
                user.set_password(user_new_pass)
                user.email_activation_code = account_activation_token.make_token(user)
                user.is_active = True
                user.save()
                request.session["reset_pass_success_msg"] = True
                return redirect(reverse('home-page'))

            request.session["reset_pass_notMatch_confirmPass"] = True
            return redirect(reverse("reset_password_page" ,kwargs={"active_code":user.email_activation_code}))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)
